from typing import Protocol, runtime_checkable
from pathlib import Path
from PIL.Image import Image
from .models import ClassificationResult
from ..result import Result


@runtime_checkable
class ClassifierPort(Protocol):
    """
    Inbound port for image classification.
    Adheres to dependency inversion principle.
    """

    def classify(self, image: Image) -> Result[ClassificationResult, Exception]:
        """
        Classifies an input image into known categories.

        Args:
            image: A PIL Image object.

        Returns:
            Result wrapping ClassificationResult or an Exception.
        """
        ...


@runtime_checkable
class ImageLoaderPort(Protocol):
    """Port for loading images from various sources."""

    def load_from_path(self, path: Path) -> Result[Image, Exception]:
        """Loads an image from the filesystem."""
        ...
