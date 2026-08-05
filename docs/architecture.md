# Architecture

## The shape

Ports and adapters. The domain knows nothing about HuggingFace, the filesystem
or the terminal; everything concrete plugs into it from outside.

```
                      ┌────────────────────────┐
                      │        main.py         │   imperative shell:
                      │  CLI, wiring, rich UI  │   builds objects, prints
                      └───────────┬────────────┘
                                  │
                      ┌───────────▼────────────┐
                      │  ClassifyImageService  │   application: one use case,
                      │       (use case)       │   load then classify
                      └───────────┬────────────┘
                                  │ depends only on Protocols
              ┌───────────────────┴───────────────────┐
              │                                       │
   ┌──────────▼──────────┐             ┌──────────────▼─────────────┐
   │   ImageLoaderPort   │             │       ClassifierPort       │  domain:
   │      (Protocol)     │             │         (Protocol)         │  interfaces
   └──────────▲──────────┘             └──────────────▲─────────────┘  and models
              │                                       │
   ┌──────────┴──────────┐             ┌──────────────┴─────────────┐
   │  LocalImageLoader   │             │ HuggingFaceSwinClassifier  │  infrastructure
   │  (PIL, filesystem)  │             │   (transformers, torch)    │
   └─────────────────────┘             └────────────────────────────┘
```

`domain/` imports `dataclasses`, `typing` and `PIL.Image` — the last only for a
type annotation. Nothing else. That is the whole point: replacing HuggingFace
with ONNX Runtime means one new class in `infrastructure/` and one changed line
in `main.py`.

## Errors are values, not exceptions

`result.py` implements a small `Result[T, E]`. Every port returns
`Result[..., Exception]` instead of raising:

```python
image_result = self._loader.load_from_path(path)
if image_result.is_failure:
    return Result.failure(image_result.error())
```

The two things that realistically go wrong here — a missing file, and a model
that will not download — are ordinary outcomes, not bugs. Putting them in the
return type means the caller cannot quietly skip them: there is no path through
`ClassifyImageService.execute` that ignores a failed load.

The trade-off, stated plainly: `unwrap()` still raises if called on a failure.
`Result` does not remove the possibility of a crash, only the possibility of an
*unnoticed* one.

## Data flow

1. `main.py` constructs `LocalImageLoader` and `HuggingFaceSwinClassifier` and
   injects both into `ClassifyImageService`. This is the only place where a
   concrete class is named.
2. `execute(path)` loads the image; on failure the error is returned unchanged.
3. The image goes to the classifier port, which returns a `ClassificationResult`
   holding an ordered list of `Prediction` value objects plus the winner.
4. `main.py` renders that as a `rich` table with confidence bars. The domain
   formats nothing.

`Prediction`, `ClassificationResult` and `ImageMetadata` are all
`@dataclass(frozen=True)`: a result cannot be edited after the fact, so the
number printed is the number the model produced.

## Model

`microsoft/swin-tiny-patch4-window7-224`, fetched from HuggingFace on first run
(~110 MB, cached afterwards). Swin computes self-attention inside shifted local
windows rather than across the whole image, which is what keeps it tractable on
CPU — measured at roughly 100 ms per image.

Weights are deliberately not vendored. They are large and versioned upstream;
the model name in `hf_adapter.py` is the pin, and committing a copy would make
the repository heavy without making it more reproducible.

## Deliberate omissions

- **No batching.** The use case classifies one image. Batching would change
  every signature to serve a case this CLI does not have.
- **No GPU path.** This targets CPU inference; CUDA branches would double the
  test matrix for a case that is not the point.
- **No async.** One blocking inference call has nothing to overlap with.
- **No model cache management.** HuggingFace's own cache is used as-is.

## Where to add things

| To add | Put it |
| --- | --- |
| Another model backend | a new adapter in `infrastructure/` satisfying `ClassifierPort` |
| Another image source (URL, camera) | a new adapter satisfying `ImageLoaderPort` |
| A new output format | `main.py` — the domain must not learn about formatting |
| A new fact about a prediction | `domain/models.py`, plus tests |

## A note on `.agent/` and `workflow_prompts/`

Those two directories are vendored AI-agent configuration, not part of the
program. They are excluded from linting and coverage in `pyproject.toml` so that
quality numbers describe this project's code rather than a copied toolkit.
