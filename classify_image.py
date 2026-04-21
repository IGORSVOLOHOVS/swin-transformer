import sys
from pathlib import Path

# Add src to path if running directly from root
sys.path.append(str(Path(__file__).parent / "src"))

from swin_classifier.main import run_classification


def main() -> None:
    """Legacy entry point wrapper for the modernized swin_classifier."""
    image_path = "data/image.png"
    if len(sys.argv) > 1:
        image_path = sys.argv[1]

    run_classification(image_path)


if __name__ == "__main__":
    main()
