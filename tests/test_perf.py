import time
from PIL import Image
from swin_classifier.infrastructure.image_loader import LocalImageLoader
from swin_classifier.infrastructure.hf_adapter import HuggingFaceSwinClassifier
from swin_classifier.application.classify_use_case import ClassifyImageService


def test_inference_latency(sample_image: Image.Image) -> None:
    """
    Measures inference latency.
    Establish a performance baseline.
    """
    # Mock pre-loaded components to measure pure inference/post-processing
    classifier = HuggingFaceSwinClassifier()

    # We use a dummy image already loaded to measure the core classify step
    start_time = time.perf_counter()
    res = classifier.classify(sample_image)
    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000
    print(f"\nLatency: {latency_ms:.2f} ms")

    assert res.is_success
    # Typically Swin-Tiny on CPU is 50-200ms
    assert latency_ms < 1000  # Sanity check
