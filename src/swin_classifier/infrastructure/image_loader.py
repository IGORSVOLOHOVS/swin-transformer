from pathlib import Path
from PIL import Image
from ..domain.interfaces import ImageLoaderPort
from ..result import Result


class LocalImageLoader(ImageLoaderPort):
    """Implementation of ImageLoaderPort for local filesystems."""

    def load_from_path(self, path: Path) -> Result[Image.Image, Exception]:
        """
        Loads and validates an image from a local path.
        Returns a Result containing the PIL Image or an Error.
        """
        try:
            if not path.exists():
                return Result.failure(FileNotFoundError(f"Image not found at: {path}"))

            image = Image.open(path).convert("RGB")
            return Result.success(image)
        except Exception as e:
            return Result.failure(e)
