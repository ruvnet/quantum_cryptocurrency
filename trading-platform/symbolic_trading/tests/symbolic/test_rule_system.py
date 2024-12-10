import pytest
from src.transformers.transformer import Transformer

class TestRuleSystem:
    @pytest.fixture
    def transformer(self):
        return Transformer()

    def test_algebraic_rules(self, transformer):
        """Test algebraic simplification rules"""
        cases = [
            ("x + 0", "x"),
            ("x * 1", "x"),
            ("x * 0", "0"),
            ("x^1", "x"),
            ("x^0", "1"),
            ("0^x", "0"),
            ("(x^n)^m", "x^(n*m)")
        ]
        
        for input_expr, expected in cases:
            result = transformer.simplify_expression(input_expr)
            assert str(result) == expected

    def test_trigonometric_rules(self, transformer):
        """Test trigonometric simplification rules"""
        # Should implement trig identities
        with pytest.raises(NotImplementedError):
            transformer.simplify_expression("sin(x)^2 + cos(x)^2")

    def test_logarithmic_rules(self, transformer):
        """Test logarithmic simplification rules"""
        # Should implement log rules
        with pytest.raises(NotImplementedError):
            transformer.simplify_expression("log(x*y)")
