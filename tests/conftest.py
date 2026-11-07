import io
import os

import numpy as np
import pytest
from PIL import Image

# huggingface_hub reads this once, on import, and nothing has imported it yet: conftest.py comes
# first. A test that reaches for weights then fails on the spot instead of fetching them, however
# pytest was started. `setdefault`, so a person can still fetch them with HF_HUB_OFFLINE=0.
os.environ.setdefault("HF_HUB_OFFLINE", "1")


@pytest.fixture
def sample_image() -> Image.Image:
    """Creates a dummy RGB image for testing."""
    image = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
    return image


@pytest.fixture
def sample_image_bytes(sample_image: Image.Image) -> bytes:
    """Returns dummy image as bytes."""
    buf = io.BytesIO()
    sample_image.save(buf, format="PNG")
    return buf.getvalue()
