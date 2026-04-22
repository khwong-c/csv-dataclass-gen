from generator.type_inferrer import infer_type, InferredType


class TestTypeInferrer:
    """Tests for the infer_type function."""

    def test_infer_type_empty_list(self):
        """Should return STRING type for an empty list."""
        result = infer_type([])
        assert result == InferredType.STRING

    def test_infer_type_all_empty(self):
        """Should return STRING type for all the values are empty."""
        result = infer_type(["", "", ""])
        assert result == InferredType.STRING

    def test_infer_type_all_empty_or_integers(self):
        """Should return STRING type with all the values are empty or integers."""
        result = infer_type(["", "1", ""])
        assert result == InferredType.STRING

    def test_infer_type_all_empty_or_float(self):
        """Should return STRING type with all the values are empty or floats."""
        result = infer_type(["", "1.1", ""])
        assert result == InferredType.STRING

    def test_infer_type_integers(self):
        """Should return INT type for a list of integers."""
        result = infer_type(["1", "2", "3"])
        assert result == InferredType.INT

    def test_infer_type_floats(self):
        """Should return FLOAT type for a list of floats."""
        result = infer_type(["1.0", "2.5", "3.3"])
        assert result == InferredType.FLOAT

    def test_infer_type_strings(self):
        """Should return STRING type for a list of non-numeric strings."""
        result = infer_type(["apple", "banana", "cherry"])
        assert result == InferredType.STRING

    def test_infer_type_mixed_integers_and_floats(self):
        """Should return FLOAT type for a mixed list of integers and floats."""
        result = infer_type(["1", "2.5", "3.0"])
        assert result == InferredType.FLOAT

    def test_infer_type_with_leading_zeros(self):
        """Should return STRING type for values with leading zeros."""
        result = infer_type(["001", "002", "003"])
        assert result == InferredType.STRING

    def test_infer_type_boolean_like_values(self):
        """Should return STRING type for boolean-like values."""
        result = infer_type(["True", "False", "yes", "no", "0", "1"])
        assert result == InferredType.STRING

    def test_infer_type_scientific_notation(self):
        """Should return FLOAT type for scientific notation values."""
        result = infer_type(["1.5e10", "2.3e-5", "3.14e2"])
        assert result == InferredType.FLOAT
