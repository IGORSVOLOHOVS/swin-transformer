"""Tests for the imperative shell.

`run_classification` constructs its adapters itself, so the only way to exercise
it without downloading a model is to substitute those two names in the module.
That is done here rather than restructuring `main.py`: the direct construction
is what makes the entry point readable, and it is the one place in the codebase
allowed to name concrete classes.

What is actually being checked is the shell's contract: on success it prints the
table and returns; on failure it reports and exits non-zero.
"""

from __future__ import annotations

import pytest

from swin_classifier import main as main_module
from swin_classifier.domain.models import ClassificationResult, Prediction
from swin_classifier.result import Result


@pytest.fixture
def predictions() -> list[Prediction]:
    return [
        Prediction(class_index=345, label="ox", confidence=0.5758),
        Prediction(class_index=349, label="ram, tup", confidence=0.0222),
    ]


@pytest.fixture
def patched(monkeypatch, sample_image, predictions):
    """Replace both adapters in main's namespace with controllable fakes."""

    def install(load: Result, classify: Result) -> None:
        monkeypatch.setattr(main_module, "LocalImageLoader", lambda: _Loader(load))
        monkeypatch.setattr(main_module, "HuggingFaceSwinClassifier", lambda: _Classifier(classify))

    class _Loader:
        def __init__(self, result: Result) -> None:
            self._result = result

        def load_from_path(self, path):
            return self._result

    class _Classifier:
        def __init__(self, result: Result) -> None:
            self._result = result

        def classify(self, image):
            return self._result

    return install


def test_prints_the_table_on_success(patched, capsys, sample_image, predictions):
    patched(
        Result.success(sample_image),
        Result.success(
            ClassificationResult(predictions=predictions, top_prediction=predictions[0])
        ),
    )

    main_module.run_classification("whatever.png")

    out = capsys.readouterr().out
    assert "Top-5 Classification Predictions" in out
    assert "ox" in out
    assert "Winner" in out


def test_reports_and_exits_when_loading_fails(patched, capsys):
    patched(Result.failure(FileNotFoundError("missing.png")), Result.success(None))

    with pytest.raises(SystemExit) as exit_info:
        main_module.run_classification("missing.png")

    assert exit_info.value.code == 1
    assert "Classification Failed" in capsys.readouterr().out


def test_reports_and_exits_when_the_model_fails(patched, capsys, sample_image):
    patched(Result.success(sample_image), Result.failure(RuntimeError("model refused")))

    with pytest.raises(SystemExit) as exit_info:
        main_module.run_classification("whatever.png")

    assert exit_info.value.code == 1


def test_main_defaults_to_the_bundled_image(monkeypatch, patched, sample_image, predictions):
    patched(
        Result.success(sample_image),
        Result.success(
            ClassificationResult(predictions=predictions, top_prediction=predictions[0])
        ),
    )
    seen: list[str] = []
    monkeypatch.setattr(main_module, "run_classification", seen.append)
    monkeypatch.setattr(main_module.sys, "argv", ["swin-classify"])

    main_module.main()

    assert seen == ["data/image.png"]


def test_main_takes_the_path_from_argv(monkeypatch):
    seen: list[str] = []
    monkeypatch.setattr(main_module, "run_classification", seen.append)
    monkeypatch.setattr(main_module.sys, "argv", ["swin-classify", "other.png"])

    main_module.main()

    assert seen == ["other.png"]
