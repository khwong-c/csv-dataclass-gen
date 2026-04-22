# tests/test_csv_analyzer.py
import csv
from pathlib import Path

import pytest
from generator.csv_analyzer import analyze_csv, CSVSchema
from generator.type_inferrer import InferredType


class TestAnalyzeCSV:
    """Tests for the `analyze_csv` function."""

    def test_valid_csv_with_default_sample_size(self, tmp_path):
        """Test analyzing a valid CSV file with the default sample size."""
        csv_path = tmp_path / "test.csv"
        csv_content = [
            "name,age,salary",
            "John,30,60000.0",
            "Jane,25,55000.0"
        ]
        csv_path.write_text("\n".join(csv_content))

        result = analyze_csv(path=csv_path)

        assert isinstance(result, CSVSchema)
        assert result.file_name == "test.csv"
        assert result.base_name == "test"
        assert result.delimiter == ","
        assert len(result.columns) == 3
        assert result.columns[0].original_name == "name"
        assert result.columns[0].inferred_type == InferredType.STRING
        assert result.columns[1].inferred_type == InferredType.INT
        assert result.columns[2].inferred_type == InferredType.FLOAT

    def test_csv_with_custom_sample_size(self, tmp_path):
        """Test analyzing a valid CSV file with a custom sample size."""
        csv_path = tmp_path / "test.csv"
        csv_content = [
            "name,age,salary",
            "John,30,60000.0",
            "Jane,25,55000.0"
        ]
        csv_path.write_text("\n".join(csv_content))

        result = analyze_csv(path=csv_path, sample_size=1)

        assert isinstance(result, CSVSchema)
        assert result.file_name == "test.csv"
        assert len(result.columns) == 3

    def test_csv_with_duplicate_columns(self, tmp_path):
        """Test analyzing a CSV file with duplicate column names."""
        csv_path = tmp_path / "test_duplicates.csv"
        csv_content = [
            "name,age,name",
            "John,30,Smith",
            "Jane,25,Doe"
        ]
        csv_path.write_text("\n".join(csv_content))

        result = analyze_csv(path=csv_path)

        assert isinstance(result, CSVSchema)
        assert result.file_name == "test_duplicates.csv"
        assert len(result.columns) == 2  # Should only keep unique columns
        assert result.columns[0].original_name == "name"
        assert result.columns[1].original_name == "age"

    def test_csv_with_nonexistent_file(self):
        """Test analyzing a CSV file that does not exist."""
        non_existent_path = Path("non_existent.csv")

        with pytest.raises(FileNotFoundError):
            analyze_csv(path=non_existent_path)

    def test_csv_with_empty_file(self, tmp_path):
        """Test analyzing an empty CSV file."""
        empty_csv_path = tmp_path / "empty.csv"
        empty_csv_path.touch()  # Create an empty file

        with pytest.raises(csv.Error):
            analyze_csv(path=empty_csv_path)
