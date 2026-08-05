import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

from ..domain.interfaces import ClassifierPort
from ..domain.models import ClassificationResult, Prediction
from ..result import Result


class HuggingFaceSwinClassifier(ClassifierPort):
    """
    Adapter for HuggingFace Transformers Swin model.
    Implements ClassifierPort.
    """

    def __init__(self, model_name: str = "microsoft/swin-tiny-patch4-window7-224"):
        self.model_name = model_name
        # Pre-loading to keep classify call focused.
        # transformers ships no annotations for from_pretrained, so mypy --strict
        # reports the call as untyped; the ignore is scoped to that one fact.
        self._processor = AutoImageProcessor.from_pretrained(model_name)  # type: ignore[no-untyped-call]
        self._model = AutoModelForImageClassification.from_pretrained(model_name)

    def classify(self, image: Image.Image) -> Result[ClassificationResult, Exception]:
        """
        Processes image through Swin Transformer and returns results.
        """
        try:
            # 1. Preprocess
            inputs = self._processor(images=image, return_tensors="pt")

            # 2. Inference
            with torch.no_grad():
                outputs = self._model(**inputs)
                logits = outputs.logits
                probs = torch.nn.functional.softmax(logits, dim=-1)

            # 3. Post-process
            top_k = 5
            top_probs, top_indices = torch.topk(probs, top_k)

            predictions = []
            for i in range(top_k):
                # Tensor.item() is typed as returning int | float | bool, so the
                # index has to be narrowed before it can be a class_index.
                idx = int(top_indices[0][i].item())
                label = str(self._model.config.id2label[idx])
                score = float(top_probs[0][i].item())
                predictions.append(Prediction(class_index=idx, label=label, confidence=score))

            result = ClassificationResult(predictions=predictions, top_prediction=predictions[0])

            return Result.success(result)

        except Exception as e:
            return Result.failure(e)
