# File: tests/test_name_sanitizer.py

from generator.name_sanitizer import sanitize_class_name, sanitize_column_names, sanitize_mod_name


class TestSanitizeClassName:
    """Test class name sanitization functionality."""

    def test_simple_name(self):
        """Test basic name conversion to PascalCase."""
        input_name = "simple_name"
        expected = "SimpleName"
        assert expected == sanitize_class_name(input_name)

    def test_name_with_special_characters(self):
        """Test handling of special characters."""
        input_name = "name@with#special!characters"
        expected = "NameWithSpecialCharacters"
        assert expected == sanitize_class_name(input_name)

    def test_name_with_hyphen_and_spaces(self):
        """Test handling of spaces and hyphens."""
        input_name = "name with-hyphen_and spaces"
        expected = "NameWithHyphenAndSpaces"
        assert expected == sanitize_class_name(input_name)

    def test_name_with_numbers(self):
        """Test handling of numbers in name."""
        input_name = "number 123 name"
        expected = "Number123Name"
        assert expected == sanitize_class_name(input_name)

    def test_name_with_leading_numbers(self):
        """Test handling of leading numbers in name."""
        input_name = "123number_name"
        expected = "Data123numberName"
        assert expected == sanitize_class_name(input_name)

    def test_name_with_numbers_and_space(self):
        """Test handling of numbers in name."""
        input_name = "123 number_name"
        expected = "Data123NumberName"
        assert expected == sanitize_class_name(input_name)

    def test_empty_name(self):
        """Test handling of empty name."""
        input_name = ""
        expected = "CSVData"
        assert expected == sanitize_class_name(input_name)

    def test_name_with_extra_spaces(self):
        """Test trimming and reducing multiple spaces."""
        input_name = "  name  with   extra spaces  "
        expected = "NameWithExtraSpaces"
        assert expected == sanitize_class_name(input_name)


class TestSanitizeColumnNames:
    """Test column name sanitization functionality."""

    def test_valid_identifiers(self):
        """Test that valid Python identifiers remain untouched."""
        input_names = ["name", "age", "salary"]
        expected = {"name": "name", "age": "age", "salary": "salary"}
        assert expected == sanitize_column_names(input_names)

    def test_reserved_keywords(self):
        """Test that Python keywords are handled properly."""
        input_names = ["class", "def", "if", "for"]
        expected = {"class": "_class", "def": "_def", "if": "_if", "for": "_for"}
        assert expected == sanitize_column_names(input_names)

    def test_invalid_identifiers(self):
        """Test that invalid identifiers are sanitized correctly."""
        input_names = ["123name", "!!age!!", "sa-lary"]
        expected = {
            "123name": "_123name",
            "!!age!!": "age",
            "sa-lary": "sa_lary",
        }
        assert expected == sanitize_column_names(input_names)

    def test_empty_string(self):
        """Test with empty strings after sanitization."""
        input_names = ["", " ", "_"]
        expected = {"": "column_0", " ": "column_1", "_": "column_2"}
        assert expected == sanitize_column_names(input_names)

    def test_duplicate_names(self):
        """Test that duplicate names are made unique."""
        input_names = ["name!", "name@", "name#"]
        expected = {"name!": "name", "name@": "name_1", "name#": "name_2"}
        assert expected == sanitize_column_names(input_names)

    def test_combined_edge_cases(self):
        """Test a combination of reserved, invalid, and duplicate names."""
        input_names = ["name", "class", "123name", "name!", "class!"]
        expected = {
            "name": "name",
            "class": "_class",
            "123name": "_123name",
            "name!": "name_1",
            "class!": "_class_1",
        }
        assert expected == sanitize_column_names(input_names)

    def test_leading_and_trailing_underscores(self):
        """Test that leading/trailing underscores are removed."""
        input_names = ["__name__", "_age_", "___salary___"]
        expected = {"__name__": "name", "_age_": "age", "___salary___": "salary"}
        assert expected == sanitize_column_names(input_names)


class TestSanitizeModName:
    """Test the sanitize_mod_name function."""

    def test_basic_snake_case_conversion(self):
        """Test basic snake_case conversion."""
        result = sanitize_mod_name("TestFile")
        assert result == "testfile"

    def test_empty_string(self):
        """Ensure empty input defaults to `csv_data`."""
        result = sanitize_mod_name("")
        assert result == "csv_data"

    def test_leading_digit(self):
        """Test names that start with a digit."""
        result = sanitize_mod_name("123file")
        assert result == "data_123file"

    def test_special_characters(self):
        """Test names with special characters."""
        result = sanitize_mod_name("file@name#test!")
        assert result == "file_name_test"

    def test_multiple_spaces(self):
        """Ensure multiple spaces are handled correctly."""
        result = sanitize_mod_name("  spaced   out  name  ")
        assert result == "spaced_out_name"

    def test_hyphen_and_underscores(self):
        """Ensure hyphens and underscores are normalized."""
        result = sanitize_mod_name("test-name_with__underscores")
        assert result == "test_name_with_underscores"

    def test_no_alphanumeric_characters(self):
        """Ensure input with no alphanumeric characters defaults to `csv_data`."""
        result = sanitize_mod_name("!@#$%^&*")
        assert result == "csv_data"
