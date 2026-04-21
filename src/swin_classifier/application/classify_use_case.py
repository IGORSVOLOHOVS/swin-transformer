from pathlib import Path
from ..domain.interfaces import ClassifierPort, ImageLoaderPort
from ..domain.models import ClassificationResult
from ..result import Result


class ClassifyImageService:
    """
    Application Service (Use Case) for classifying an image.
    Orchestrates infrastructure components to achieve the domain goal.
    """

    def __init__(self, loader: ImageLoaderPort, classifier: ClassifierPort):
        self._loader = loader
        self._classifier = classifier

    def execute(self, image_path: str) -> Result[ClassificationResult, Exception]:
        """
        Executes the classification flow: Load -> Classify.
        """
        path = Path(image_path)

        # 1. Load Image
        image_result = self._loader.load_from_path(path)
        if image_result.is_failure:
            return Result.failure(image_result.error())

        # 2. Classify Image
        image = image_result.unwrap()
        classification_result = self._classifier.classify(image)

        return classification_result
