import io

import numpy as np
import pytest
from PIL import Image


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
