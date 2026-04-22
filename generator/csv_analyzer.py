"""CSV/TSV file analysis and schema inference."""

import csv
from csv import Dialect
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Counter, Callable

from logging import getLogger

from .type_inferrer import InferredType, infer_type
from .name_sanitizer import sanitize_column_names, sanitize_class_name, sanitize_mod_name

logger = getLogger(__name__)


@dataclass
class ColumnInfo:
    """Information about a CSV column."""
    original_name: str
    sanitized_name: str
    inferred_type: InferredType

    @property
    def converter(self) -> Callable[[str], str | int | float]:
        """Get value converter for loading."""
        if self.inferred_type == InferredType.INT:
            return int
        elif self.inferred_type == InferredType.FLOAT:
            return float
        return str

    @property
    def converter_name(self) -> str:
        return self.converter.__name__


@dataclass
class CSVSchema:
    """Complete schema information for a CSV file."""
    file_name: str
    base_name: str
    delimiter: str
    columns: List[ColumnInfo]
    duplicated_fields: List[str] = field(default_factory=list)

    @property
    def class_name(self) -> str:
        """Generate the class name from the file/given name."""
        return sanitize_class_name(self.base_name)

    @property
    def function_name(self) -> str:
        """Generate the loader function name from the file/given name."""
        return f"load_{self.module_name}"

    @property
    def module_name(self) -> str:
        """Generate the modul name from the file/given name."""
        return sanitize_mod_name(self.base_name)


class CSVSchemaAnalyzer:
    def __init__(
            self, path: Path,
            sample_size: int = 256,
            base_name: str | None = None,
    ):
        """
        Initialize analyzer.

        Args:
            sample_size: Number of rows to be sampled for type inference
        """
        self.sample_size = sample_size
        self.file_path = path

        self.dialect = self._sniff_dialect()
        self.delimiter = self.dialect.delimiter
        self.unique_fields, self.duplicated_fields = self._check_duplicated_fields()
        self.field_mapping = sanitize_column_names(self.unique_fields)

        self.grouped_samples = self._group_samples_by_fields(
            self._read_samples(self.sample_size)
        )

        self.columns_info = {
            sanitized_name: ColumnInfo(
                original_name=original_name,
                sanitized_name=sanitized_name,
                inferred_type=infer_type(self.grouped_samples[original_name]),
            )
            for original_name, sanitized_name in self.field_mapping.items()
        }
        self.schema = CSVSchema(
            file_name=self.file_path.name,
            base_name=base_name or self.file_path.stem,
            delimiter=self.delimiter,
            columns=list(self.columns_info.values()),
            duplicated_fields=self.duplicated_fields,
        )

    def _sniff_dialect(self) -> type[Dialect]:
        """Sniff dialect by sampling the beginning of a CSV file."""
        sample_size = min(self.sample_size, 32)
        with self.file_path.open('r', encoding='utf-8') as f:
            content = []
            for i, line in enumerate(f):
                if i >= sample_size:
                    break
                content.append(line)
            return csv.Sniffer().sniff('\n'.join(content))

    def _check_duplicated_fields(self) -> tuple[list[str], list[str]]:
        """Return unique fields and duplicated fields."""
        with self.file_path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f, dialect=self.dialect)
            fields = Counter(reader.fieldnames)
            return list(fields.keys()), [
                field for field, count in fields.items()
                if count > 1
            ]

    def _read_samples(self, sample_size: int) -> list[dict[str, str]]:
        """Read sample rows from the file."""
        result = []
        with self.file_path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f, dialect=self.dialect)
            for i, row in enumerate(reader):
                if i >= sample_size:
                    break
                result.append(row)
            return result

    def _group_samples_by_fields(self, samples: list[dict[str, str]]) -> dict[str, list[str]]:
        """Group samples by field names."""
        return {
            field: [sample.get(field, "") for sample in samples]
            for field in self.unique_fields
        }


def analyze_csv(path: Path, sample_size: int = 1000, base_name: str | None = None) -> CSVSchema:
    """Convenience function to analyze a CSV file."""
    analyzer = CSVSchemaAnalyzer(
        path=path,
        sample_size=sample_size,
        base_name=base_name,
    )
    return analyzer.schema
