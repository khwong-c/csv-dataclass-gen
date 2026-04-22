import csv
import importlib
import importlib.abc
import importlib.util
from pathlib import Path

import pytest
from generator.code_generator import CodeGenerator
from generator.csv_analyzer import analyze_csv
from dataclasses import asdict


class TestE2EWithReconstruction:
    """Test code generation and loading function by CSV reconstruction."""

    class StringLoader(importlib.abc.SourceLoader):
        """
        Helper class to load generated code as string into a module.
        """

        def __init__(self, data):
            self.data = data

        def get_source(self, fullname):
            return self.data

        def get_data(self, path):
            return self.data.encode("utf-8")

        def get_filename(self, fullname):
            return "<not a real path>/" + fullname + ".py"

    @pytest.mark.parametrize("csv_file_name", [
        "test_data.csv",
        "test_data.tsv",
    ])
    def test_reconstruct_csv_file(self, tmp_path, csv_file_name):
        """
        Test if load_time_values can reconstruct the data rows from the original CSV
        and compare it with the reconstructed file.
        """
        original_csv_file = Path(__file__).parent / "data" / csv_file_name
        reconstructed_csv_file = tmp_path / "reconstructed.csv"

        # Read the schema of the original CSV file
        schema = analyze_csv(path=original_csv_file)

        # Get the fieldnames and column map from the schema for CSV reconstruction
        fieldnames = [
            col.original_name
            for col in schema.columns
        ]
        column_map = {col.sanitized_name: col.original_name for col in schema.columns}

        # Generate the dataclass with loading code and execute it
        generated_code = CodeGenerator(schema, output_dir='-').generate_dataclass_code()

        # Import the generated code as a module.
        code_loader = self.StringLoader(generated_code)
        spec = importlib.util.spec_from_loader("generated_module", code_loader, origin="built-in")
        assert spec is not None, "Failed to create module spec."
        assert spec.loader is not None, "Module spec has no loader."
        generated_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_module)

        # We expect the following objects in the generated module:
        assert "TestData" in dir(generated_module), "Dataclass not found in generated code."
        assert "load_test_data" in dir(generated_module), "Loader Function not found in generated code."
        load_test_data = generated_module.load_test_data

        # Reconstruct a CSV file from the loaded data for comparison
        with reconstructed_csv_file.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=schema.delimiter)
            writer.writeheader()
            for loaded_row in load_test_data(original_csv_file):
                loaded_dict = asdict(loaded_row)
                reconstructed_dict = {
                    column_map.get(key, key): value
                    for key, value in loaded_dict.items()
                }
                writer.writerow(reconstructed_dict)

        # Verify the reconstructed CSV matches the original CSV
        with original_csv_file.open("r") as orig_f, reconstructed_csv_file.open("r") as recon_f:
            for original_line, reconstructed_line in zip(orig_f, recon_f):
                assert original_line.strip() == reconstructed_line.strip()
