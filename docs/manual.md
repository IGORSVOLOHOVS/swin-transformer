# Manual

```powershell
.\recipe.ps1 run [<image>]
```

| argument | what it does |
| --- | --- |
| `<image>` | the path of the image to classify; `data/image.png` when left out |

The program loads the image, converts it to RGB and runs Swin-Tiny on the CPU. It prints a table of the five most likely labels with their scores and a bar for each, then the winner with its class index. The labels are the 1000 categories of ImageNet-1k, so a picture of something outside them still gets a confident answer.

It exits 0 on success. A missing file, a directory or a file that is not an image prints a `Classification Failed` panel and exits 1.

## The test that loads the model

`tests/test_perf.py` is marked `model`: it loads the real weights, so `addopts` in `pyproject.toml` leaves it out of `.\recipe.ps1 test` and of every gate. `tests/conftest.py` also sets `HF_HUB_OFFLINE`, so a test that reaches for weights fails at once instead of fetching them.

Run it by hand, from weights already in the cache:

```powershell
uv run --frozen python -m pytest -m model --no-cov -s
```

On a machine that has no weights yet, set `$env:HF_HUB_OFFLINE = '0'` first.

## Measurements

```powershell
uv run --frozen python -m pytest benchmarks --benchmark-only --no-cov
uv run --frozen python scripts/collect_quality_metrics.py --output quality-report.json
```

The benchmarks stub the model, so they measure this repository's code and not the network. The second command gathers the numbers `docs/quality-iso25010.md` cites.
