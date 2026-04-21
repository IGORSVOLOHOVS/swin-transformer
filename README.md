# Swin Transformer Image Classifier

A professional, domain-driven Python implementation of image classification using the Swin Transformer (`microsoft/swin-tiny-patch4-window7-224`).

## 🚀 Key Features
- **Clean Architecture**: Strict separation of concerns (Domain, Application, Infrastructure).
- **DDD Principles**: Ubiquitous language, Value Objects, Entities, and Ports/Adapters.
- **Monadic Error Flow**: explicit error handling via `Result` pattern (no exceptions).
- **Rich Observability**: Professional terminal UI and structured logging using `rich`.
- **High Performance**: Optimized inference pipeline with a latency baseline of ~100ms on CPU.
- **Strict Typing**: Python 3.10+ type hints with `mypy --strict` compliance.

## 📁 Structure
- `src/swin_classifier/`
  - `domain/`: Core models and interfaces (Protocols).
  - `application/`: Use cases (ClassifyImageService).
  - `infrastructure/`: External integrations (HuggingFace, Local IO).
  - `main.py`: Entry point and CLI logic.
  - `result.py`: Monadic Result type implementation.
- `tests/`: Pytest suite with fixtures and performance benchmarks.
- `docs/api/`: Auto-generated API documentation.

## 🖼️ Example Result

### Input Image
![Classified Image](data/image.png)

### Classification Output
```text
🔍 Processing image: data/image.png
          Top-5 Classification Predictions
┏━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Rank ┃ Label            ┃  Score ┃ Confidence Bar ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│  1   │ ox               │ 0.5758 │ ███████████    │
│  2   │ ram, tup         │ 0.0222 │                │
│  3   │ kuvasz           │ 0.0093 │                │
│  4   │ llama            │ 0.0082 │                │
│  5   │ golden retriever │ 0.0056 │                │
└──────┴──────────────────┴────────┴────────────────┘
╭────────────────────────────╮
│ 🏆 Winner: ox (Index: 345) │
╰────────────────────────────╯
```

## 🛠️ Usage

### Installation
Ensure you have the dependencies installed:
```bash
pip install transformers torch Pillow numpy rich pdoc pytest
```

### Running Classification
Classify the default image:
```bash
python classify_image.py
```

Classify a specific image:
```bash
python classify_image.py data/image.png
```

### Testing & Quality
Run unit tests:
```bash
$env:PYTHONPATH='src'; python -m pytest tests/
```

Run performance benchmarks:
```bash
$env:PYTHONPATH='src'; python -m pytest tests/test_perf.py -s
```

## 📊 Performance Baseline
- **Model**: Swin-Tiny
- **Device**: CPU
- **Avg Latency**: ~101 ms
- **Confidence**: Structured Top-5 output.

## 📝 License
MIT
