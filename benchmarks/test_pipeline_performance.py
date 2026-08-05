"""Point 7: benchmarks, so a performance regression shows up as a number.

What is measured here is everything the pipeline does *around* the model:
decoding an image off disk, converting it to RGB, and the use case that wires
loading to classification. On CPU that work is not free, and unlike the model
it is entirely this project's own code - so it is the part a change here can
actually make slower.

The model is deliberately excluded. `HuggingFaceSwinClassifier()` downloads
several hundred megabytes of weights on first use, so a figure that includes it
measures the network and the disk cache, not the code.

`tests/test_perf.py` also times inference, but with one `perf_counter` call, no
warm-up and no repetitions - a single sample of a noisy quantity. These
benchmarks report a distribution instead.

    pytest benchmarks --benchmark-only
    pytest benchmarks --benchmark-only --benchmark-compare
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pytest
from PIL import Image

from swin_classifier.application.classify_use_case import ClassifyImageService
from swin_classifier.domain.models import ClassificationResult, Prediction
from swin_classifier.infrastructure.image_loader import LocalImageLoader
from swin_classifier.result import Result


class StubClassifier:
    """A classifier that answers instantly.

    The point is to leave only the orchestration in the measurement: with a real
    model the use case's own cost would be lost in the noise of inference.
    """

    _answer = Prediction(class_index=0, label="stub", confidence=1.0)

    def classify(self, image: Image.Image) -> Result[ClassificationResult, Exception]:
        return Result.success(
            ClassificationResult(predictions=[self._answer], top_prediction=self._answer)
        )


@pytest.fixture(scope="module")
def images(tmp_path_factory: pytest.TempPathFactory) -> dict[int, Path]:
    """One PNG per size, written once and reused across benchmarks."""
    directory = tmp_path_factory.mktemp("benchmark-images")
    written: dict[int, Path] = {}
    for side in (64, 224, 1024):
        pixels = np.random.randint(0, 255, (side, side, 3), dtype=np.uint8)
        path = directory / f"{side}.png"
        Image.fromarray(pixels).save(path)
        written[side] = path
    return written


@pytest.mark.parametrize("side", [64, 224, 1024])
def test_image_loading_scales(benchmark: Any, images: dict[int, Path], side: int) -> None:
    """Decoding and RGB conversion, the cost paid before the model sees anything."""
    loader = LocalImageLoader()

    result = benchmark(loader.load_from_path, images[side])

    assert result.is_success


def test_missing_file_is_cheap(benchmark: Any, tmp_path: Path) -> None:
    """The failure path should cost a stat call, not an exception unwind."""
    loader = LocalImageLoader()
    missing = tmp_path / "does-not-exist.png"

    result = benchmark(loader.load_from_path, missing)

    assert result.is_failure


def test_use_case_overhead(benchmark: Any, images: dict[int, Path]) -> None:
    """Load plus orchestration, with the model stubbed out."""
    service = ClassifyImageService(LocalImageLoader(), StubClassifier())
    path = str(images[224])

    result = benchmark(service.execute, path)

    assert result.is_success
