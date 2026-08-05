"""Tests for the filesystem adapter.

Only the missing-file branch was covered before. The success path and the
"exists but is not an image" path are the two that decide whether a real run
gets off the ground, so both are exercised here against real files.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from swin_classifier.infrastructure.image_loader import LocalImageLoader


class TestLocalImageLoader:
    def test_loads_a_real_file(self, tmp_path: Path, sample_image: Image.Image):
        target = tmp_path / "picture.png"
        sample_image.save(target)

        result = LocalImageLoader().load_from_path(target)

        assert result.is_success
        assert result.unwrap().size == sample_image.size

    def test_converts_to_rgb(self, tmp_path: Path):
        # A greyscale source must still arrive as three channels, because the
        # processor downstream assumes RGB.
        target = tmp_path / "grey.png"
        Image.new("L", (64, 64), color=128).save(target)

        result = LocalImageLoader().load_from_path(target)

        assert result.is_success
        assert result.unwrap().mode == "RGB"

    def test_missing_file_is_a_failure_not_an_exception(self, tmp_path: Path):
        result = LocalImageLoader().load_from_path(tmp_path / "nope.png")

        assert result.is_failure
        assert isinstance(result.error(), FileNotFoundError)
        assert "nope.png" in str(result.error())

    def test_a_file_that_is_not_an_image_fails_cleanly(self, tmp_path: Path):
        target = tmp_path / "not-an-image.png"
        target.write_text("this is plain text", encoding="utf-8")

        result = LocalImageLoader().load_from_path(target)

        # The point is that it comes back as a Result, not as a raised
        # UnidentifiedImageError escaping the adapter.
        assert result.is_failure
        assert isinstance(result.error(), Exception)

    def test_a_directory_fails_cleanly(self, tmp_path: Path):
        result = LocalImageLoader().load_from_path(tmp_path)

        assert result.is_failure
        assert isinstance(result.error(), Exception)
