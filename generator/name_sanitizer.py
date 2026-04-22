"""Column name sanitization for Python identifiers."""

import re
from keyword import iskeyword as is_keyword, issoftkeyword as is_soft_keyword


def sanitize_snake_case(name: str) -> str:
    """
    Sanitize a filename into snake_case.
    """
    name = name.strip()
    # Replace special chars, hyphens, underscores and any space characters with spaces
    name = re.sub(r'[\W\s\-_]', ' ', name, flags=re.UNICODE)
    # Fuse multiple spaces with a single space
    name = re.sub(r' +', ' ', name).lower()
    return "_".join(
        word
        for word in name.split(" ")
        if word
    )


def sanitize_column_names(names: list[str]) -> dict[str, str]:
    """
        Sanitize a list of CSV column names to valid Python identifiers in snake_case.
        All leading and trailing "_" are removed.
        The output is a dictionary mapping original names to sanitized names.

        Handles:
        - Invalid identifiers / Reserved keywords: replace special chars with '_'
        - Empty names: generate 'column_0', 'column_1', etc.
        - Duplicates: append '_1', '_2', etc.

        Args:
            names: List of column names from the CSV header.

        Returns:
            List of sanitized Python identifiers.
    """
    seen_names = {}

    def _sanitize_name(name: str, index: int = 0) -> str:
        """Sanitize one column name."""
        name = sanitize_snake_case(name)

        # If nothing left after cleaning, use indexed column name
        if not name:
            return f'column_{index}'

        # Handle leading digits or python keywords - prepend '_'
        if name[0].isdigit() or is_keyword(name) or is_soft_keyword(name):
            name = f'_{name}'
        return name

    def _make_unique(name: str) -> str:
        """Ensure the name is unique by appending suffix if needed."""
        if name not in seen_names:
            seen_names[name] = 0
            return name

        # Duplicate found - append _2, _3, etc.
        seen_names[name] += 1
        return f'{name}_{seen_names[name]}'

    return {
        name: _make_unique(_sanitize_name(name, i))
        for i, name in enumerate(names)
    }


def sanitize_class_name(name: str) -> str:
    """
    Sanitize a filename to a valid Python class name in PascalCase.
    If the class name starts with a digit, it is prefixed with "Data".
    If the sanitized name is empty, it defaults to "CSVData".
    """
    name = name.strip()
    # Replace special chars, hyphens, underscores and any space characters with spaces
    name = re.sub(r'[\W\s\-_]', ' ', name, flags=re.UNICODE)
    # Fuse multiple spaces with a single space
    name = re.sub(r' +', ' ', name).lower()
    joined = "".join(
        word.capitalize()
        for word in name.split(" ")
        if word
    )
    if not joined:
        return "CSVData"
    if joined and joined[0].isdigit():
        return f"Data{joined}"
    return joined


def sanitize_mod_name(name: str) -> str:
    """
    Sanitize a filename to a valid Python class name in snake_case.
    If the class name starts with a digit, it is prefixed with "data".
    If the sanitized name is empty, it defaults to "csv_data".
    """
    snake_case = sanitize_snake_case(name)
    if not snake_case:
        return "csv_data"
    if snake_case and snake_case[0].isdigit():
        return f"data_{snake_case}"
    return snake_case
