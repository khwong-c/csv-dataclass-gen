import re
from enum import Enum


class InferredType(Enum):
    """Represents the inferred type of the column."""
    INT = 'int'
    FLOAT = 'float'
    STRING = 'str'


class TypeInferrer:
    """Infer Python data types from CSV string values."""

    @staticmethod
    def infer(values: list[str]) -> InferredType:
        """
        Infer the type from a list of string values.

        Returns:
            type_annotation: InferredType
        """
        if not values:
            return InferredType.STRING
        # Check for integer
        if TypeInferrer._is_integer(values):
            return InferredType.INT
        # Check for float
        if TypeInferrer._is_float(values):
            return InferredType.FLOAT
        # Default to string
        return InferredType.STRING

    @staticmethod
    def _bi_integer_conversion(value: str) -> bool:
        """Checking if the value is an integer by converting a string to an integer and back to string."""
        v = value.strip()
        if not v.isdigit():
            return False
        return str(int(v)) == v

    @staticmethod
    def _tri_float_conversion(value: str) -> bool:
        """
        Checking if the value is a float by converting a string to float back and forth for 3 times.
        It's done to avoid precision issues with floating-point arithmetic.
        """
        try:
            v = float(value.strip())
            return float(str(v)) == v
        except ValueError:
            return False

    @staticmethod
    def _integers_with_leading_zeros(value: str) -> bool:
        """
        Checking if the values are integers with leading zeros.
        They shall not be considered as floats.
        """
        if value.isdigit() and re.match(r'^0+\d+', value):
            return True
        return False

    @staticmethod
    def _is_integer(values: list[str]) -> bool:
        return all(TypeInferrer._bi_integer_conversion(v) for v in values)

    @staticmethod
    def _is_float(values: list[str]) -> bool:
        return all(
            TypeInferrer._tri_float_conversion(v) and
            not TypeInferrer._integers_with_leading_zeros(v)
            for v in values
        )


def infer_type(values: list[str]) -> InferredType:
    """Convenience function to infer type from values."""
    return TypeInferrer.infer(values)
