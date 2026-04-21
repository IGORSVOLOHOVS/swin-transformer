import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.traceback import install

from .infrastructure.image_loader import LocalImageLoader
from .infrastructure.hf_adapter import HuggingFaceSwinClassifier
from .application.classify_use_case import ClassifyImageService

# Ensure UTF-8 output for Windows compatibility (rich icons)
if sys.stdout.encoding.lower() != "utf-8":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Install rich traceback for professional error reporting
install(show_locals=True)


def run_classification(image_path: str) -> None:
    console = Console()

    with console.status("[bold green]Initializing Swin Transformer...", spinner="dots"):
        # Dependency Injection
        loader = LocalImageLoader()
        classifier = HuggingFaceSwinClassifier()
        service = ClassifyImageService(loader, classifier)

    console.print(f"🔍 [bold cyan]Processing image:[/bold cyan] {image_path}")

    result = service.execute(image_path)

    if result.is_failure:
        console.print(
            Panel(
                f"[bold red]Error:[/bold red] {result.error()}",
                title="Classification Failed",
                border_style="red",
            )
        )
        sys.exit(1)

    classification = result.unwrap()
    top = classification.top_prediction

    # Professional Output Table
    table = Table(title="Top-5 Classification Predictions", header_style="bold magenta")
    table.add_column("Rank", justify="center", style="dim")
    table.add_column("Label", style="bold green")
    table.add_column("Score", justify="right")
    table.add_column("Confidence Bar")

    for i, pred in enumerate(classification.predictions, 1):
        bar = "█" * int(pred.confidence * 20)
        table.add_row(
            str(i), pred.label, f"{pred.confidence:.4f}", f"[blue]{bar}[/blue]"
        )

    console.print(table)
    console.print(
        Panel(
            f"🏆 [bold]Winner:[/bold] [green]{top.label}[/green] (Index: {top.class_index})",
            expand=False,
            border_style="green",
        )
    )


if __name__ == "__main__":
    # Internal entry point - usually called by root classify_image.py
    if len(sys.argv) > 1:
        run_classification(sys.argv[1])
    else:
        run_classification("data/image.png")
