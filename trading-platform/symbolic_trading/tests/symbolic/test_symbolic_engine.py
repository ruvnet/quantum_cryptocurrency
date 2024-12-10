import pytest
from src.utils.expression_tree import ExpressionNode, OperatorNode, ConstantNode, VariableNode
from src.transformers.transformer import Transformer

class TestSymbolicEngine:
    @pytest.fixture
    def transformer(self):
        return Transformer()

    def test_symbolic_addition(self, transformer):
        """Test symbolic addition with variables"""
        expr = "x + y"
        result = transformer.simplify_expression(expr)
        assert str(result) == "x + y"
        
        # Test commutativity
        expr2 = "y + x"
        result2 = transformer.simplify_expression(expr2)
        assert str(result) == str(result2)

    def test_symbolic_multiplication(self, transformer):
        """Test symbolic multiplication with variables"""
        expr = "x * y"
        result = transformer.simplify_expression(expr)
        assert str(result) == "x * y"
        
        # Test distributive property
        expr2 = "x * (y + z)"
        result2 = transformer.simplify_expression(expr2)
        assert str(result2) == "(x * y) + (x * z)"

    def test_symbolic_power(self, transformer):
        """Test symbolic powers and exponents"""
        expr = "x^n"
        result = transformer.parse_expression(expr)
        assert isinstance(result, OperatorNode)
        assert result.operator == '^'
        
        # Test power rules
        expr2 = "x^(m+n)"
        result2 = transformer.parse_expression(expr2)
        assert isinstance(result2, OperatorNode)

    def test_symbolic_functions(self, transformer):
        """Test symbolic function operations"""
        # Test composition
        expr = "f(g(x))"
        with pytest.raises(NotImplementedError):
            transformer.parse_expression(expr)  # Should implement function composition

    def test_symbolic_derivatives(self, transformer):
        """Test symbolic derivatives with chain rule"""
        expr = "(x^2 + y^2)^n"
        derivative = transformer.differentiate_expression(expr, 'x')
        assert "2" in str(derivative)
        assert "x" in str(derivative)
        assert "n" in str(derivative)

    def test_symbolic_integration(self, transformer):
        """Test symbolic integration with variables"""
        expr = "n*x^n"
        integral = transformer.integrate_expression(expr, 'x')
        assert "n" in str(integral)
        assert "x" in str(integral)
        assert "(n + 1)" in str(integral)

    def test_symbolic_substitution(self, transformer):
        """Test symbolic substitution with expressions"""
        expr = "x^2 + y^2"
        substituted = transformer.substitute_expression(expr, 'x', 'sin(t)')
        assert "sin(t)" in str(substituted)
