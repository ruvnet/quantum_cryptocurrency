import pytest
from src.transformers.transformer import Transformer

class TestRuleSystem:
    @pytest.fixture
    def transformer(self):
        return Transformer()


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
import pytest
from src.transformers.transformer import Transformer

class TestRuleSystem:
    @pytest.fixture
    def transformer(self):
        return Transformer()

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
