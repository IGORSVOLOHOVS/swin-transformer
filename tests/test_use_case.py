"""Tests for the application layer.

`ClassifyImageService` had no coverage at all: it is the one place where the
load-then-classify sequence and its failure paths are decided, and it was
verified only indirectly by the end-to-end latency test, which needs a real
model download.

Because the service depends on Protocols rather than concrete classes, these
tests need no model, no network and no files - two small fakes are enough. That
is the practical payoff of the ports-and-adapters layout.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from swin_classifier.application.classify_use_case import ClassifyImageService
from swin_classifier.domain.models import ClassificationResult, Prediction
from swin_classifier.result import Result


class FakeLoader:
    """An ImageLoaderPort that returns whatever it was told to."""

    def __init__(self, result: Result) -> None:
        self._result = result
        self.calls: list[Path] = []

    def load_from_path(self, path: Path) -> Result:
        self.calls.append(path)
        return self._result


class FakeClassifier:
    """A ClassifierPort that returns whatever it was told to."""

    def __init__(self, result: Result) -> None:
        self._result = result
        self.calls: list[Image.Image] = []

    def classify(self, image: Image.Image) -> Result:
        self.calls.append(image)
        return self._result


@pytest.fixture
def prediction() -> Prediction:
    return Prediction(class_index=42, label="ox", confidence=0.57)


@pytest.fixture
def classification(prediction: Prediction) -> ClassificationResult:
    return ClassificationResult(predictions=[prediction], top_prediction=prediction)


class TestHappyPath:
    def test_returns_the_classification(self, sample_image, classification):
        service = ClassifyImageService(
            FakeLoader(Result.success(sample_image)),
            FakeClassifier(Result.success(classification)),
        )
        result = service.execute("whatever.png")
        assert result.is_success
        assert result.unwrap() is classification

    def test_passes_the_loaded_image_to_the_classifier(self, sample_image, classification):
        classifier = FakeClassifier(Result.success(classification))
        service = ClassifyImageService(FakeLoader(Result.success(sample_image)), classifier)
        service.execute("whatever.png")
        assert classifier.calls == [sample_image]

    def test_converts_the_path_argument_to_a_path(self, sample_image, classification):
        loader = FakeLoader(Result.success(sample_image))
        service = ClassifyImageService(loader, FakeClassifier(Result.success(classification)))
        service.execute("some/dir/image.png")
        assert loader.calls == [Path("some/dir/image.png")]


class TestFailurePaths:
    def test_load_failure_short_circuits(self, classification):
        classifier = FakeClassifier(Result.success(classification))
        service = ClassifyImageService(
            FakeLoader(Result.failure(FileNotFoundError("missing.png"))), classifier
        )
        result = service.execute("missing.png")

        assert result.is_failure
        assert isinstance(result.error(), FileNotFoundError)
        # The important part: a failed load must not reach the model.
        assert classifier.calls == []

    def test_classifier_failure_is_propagated(self, sample_image):
        boom = RuntimeError("model refused to load")
        service = ClassifyImageService(
            FakeLoader(Result.success(sample_image)), FakeClassifier(Result.failure(boom))
        )
        result = service.execute("whatever.png")

        assert result.is_failure
        assert result.error() is boom


class TestResultSemantics:
    def test_unwrap_on_failure_raises(self):
        with pytest.raises(ValueError, match="unwrap on Failure"):
            Result.failure(Exception("x")).unwrap()

    def test_error_on_success_raises(self):
        with pytest.raises(ValueError, match="error on Success"):
            Result.success("x").error()

    def test_map_applies_only_to_success(self):
        assert Result.success(2).map(lambda v: v * 3).unwrap() == 6

    def test_map_leaves_failure_untouched(self):
        failure = Result.failure(ValueError("nope"))
        mapped = failure.map(lambda v: v * 3)
        assert mapped.is_failure
        assert isinstance(mapped.error(), ValueError)

    def test_repr_shows_the_state(self):
        assert "success=True" in repr(Result.success(1))
        assert "success=False" in repr(Result.failure(Exception("e")))


class TestDomainModels:
    def test_classification_result_is_frozen(self, classification):
        with pytest.raises(AttributeError):
            classification.top_prediction = None

    def test_prediction_is_frozen(self, prediction):
        with pytest.raises(AttributeError):
            prediction.confidence = 1.0
