import pytest
from pathlib import Path
from swin_classifier.result import Result
from swin_classifier.domain.models import Prediction
from swin_classifier.infrastructure.image_loader import LocalImageLoader


def test_result_success() -> None:
    res: Result[str] = Result.success("test")
    assert res.is_success
    assert res.unwrap() == "test"


def test_result_failure() -> None:
    res: Result[str] = Result.failure(Exception("fail"))
    assert res.is_failure
    assert isinstance(res.error(), Exception)


def test_local_image_loader_missing_file() -> None:
    loader = LocalImageLoader()
    res = loader.load_from_path(Path("non_existent.png"))
    assert res.is_failure
    assert isinstance(res.error(), FileNotFoundError)


@pytest.mark.parametrize(
    "index, label, confidence",
    [
        (1, "cat", 0.9),
        (2, "dog", 0.8),
    ],
)
def test_prediction_model(index: int, label: str, confidence: float) -> None:
    pred = Prediction(class_index=index, label=label, confidence=confidence)
    assert pred.class_index == index
    assert pred.label == label
    assert pred.confidence == confidence
