import pytest
from src.transformers.transformer import Transformer

class TestPatternMatching:
    @pytest.fixture
    def transformer(self):
        return Transformer()

    def test_match_polynomials(self, transformer):
        """Test polynomial pattern matching"""
        expr = "x^2 + 2*x + 1"
        analysis = transformer.analyze_expression(expr)
        assert analysis['is_polynomial']
        assert analysis['degree'] == 2

    def test_match_rational_functions(self, transformer):
        """Test rational function pattern matching"""
        expr = "(x^2 + 1)/(x + 1)"
        analysis = transformer.analyze_expression(expr)
        assert not analysis['is_polynomial']
        
    def test_match_trigonometric(self, transformer):
        """Test trigonometric pattern matching"""
        expr = "sin(x)^2 + cos(x)^2"
        # Should recognize trigonometric identity
        with pytest.raises(NotImplementedError):
            transformer.simplify_expression(expr)

    def test_match_exponential(self, transformer):
        """Test exponential pattern matching"""
        expr = "e^x + e^(2*x)"
        # Should recognize exponential patterns
        with pytest.raises(NotImplementedError):
            transformer.simplify_expression(expr)
