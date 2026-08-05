from dataclasses import dataclass


@dataclass(frozen=True)
class Prediction:
    """Value object representing a single model prediction."""

    class_index: int
    label: str
    confidence: float


@dataclass(frozen=True)
class ClassificationResult:
    """Entity representing the result of a classification task."""

    predictions: list[Prediction]
    top_prediction: Prediction


@dataclass(frozen=True)
class ImageMetadata:
    """Metadata about the processed image."""

    width: int
    height: int
    channels: int
    format: str
