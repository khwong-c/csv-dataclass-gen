# CSV Dataclass Generator

Generate Python dataclasses and loader functions from CSV/TSV files.

## Features

- **Automatic Type Inference**: Detects `int`, `float`, and `str` types based on a sample of rows.
- **Dialect Detection**: Automatically identifies CSV delimiters (including TSV).
- **Name Sanitization**: Converts CSV column headers into valid Python identifiers.
- **Iterator Loading**: Generates a loading generator that yields dataclass instances, suitable for larger datasets.

## Installation

```bash
pip install csv-dataclass-gen
```

## Usage

### Command Line Interface (CLI)

The package provides a `csv-dataclass-gen` command.

```bash
# Generate code to stdout
csv-dataclass-gen data.csv

# Generate code and save to a directory
csv-dataclass-gen data.csv --output ./generated_models/

# Specify a custom class name and sample size for type inference
csv-dataclass-gen data.csv --name my_custom_data --sample-size 500
```

#### CLI Help Message:

```text
Usage: csv-dataclass-gen [OPTIONS] INPUT_FILE

  Generate dataclass and loader code from CSV files.

Options:
  -o, --output TEXT          Output directory for generated files. "-" outputs
                             the result to stdout.
  -s, --sample-size INTEGER  Number of rows to sample for type inference
  -n, --name TEXT            Alternative name for the generated name. Snake
                             case / spaced words is recommended.
  --help                     Show this message and exit.
```

#### Arguments:
- `INPUT_FILE`: Path to the CSV/TSV file (required).

### Example Generated Code

Given a CSV like `users.csv`:
```csv
id,user_name,score
1,alice,95.5
2,bob,88.0
```

The generator will produce:
```python
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
import csv

@dataclass
class Users:
    id: int  # Original: "id"
    user_name: str  # Original: "user_name"
    score: float  # Original: "score"

def load_users(csv_path: Path, max_rows: int | None = None, delimiter: str = ',') -> Iterator[Users]:
    # ... loading logic ...
    pass
```

## Development

### Dependencies

This project uses [uv](https://github.com/astral-sh/uv) for dependency management, but it can also be installed using standard tools.

```bash
uv sync --all-groups
```

### Running Tests

We use `pytest` for testing.

```bash
uv run pytest
```

Tests include:
- `tests/test_name_sanitizer.py`: Logic for sanitizing names into different formats.
- `tests/test_type_inferrer.py`: Logic for detecting data types.
- `tests/test_csv_analyzer.py`: Logic for CSV structure analysis.
- `tests/test_code_gen_e2e.py`: End-to-end tests that generate code and verify it by reconstructing the original CSV.

## License

MIT License – see the [LICENSE](LICENSE) file for details.
