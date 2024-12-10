import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from src.utils.expression_tree import ExpressionNode, OperatorNode, ConstantNode, VariableNode
from src.transformers.transformer import Transformer
from src.parser.parser import Parser
from src.llm_integration.openrouter_client import OpenRouterClient
from src.trading.trader import Trader

# Fixtures for common test setup
@pytest.fixture
def mock_openrouter():
    with patch('src.llm_integration.openrouter_client.OpenRouterClient') as mock:
        client = mock.return_value
        client.generate_response = AsyncMock(return_value="Test response")
        yield client

@pytest.fixture
def mock_env_vars():
    env_vars = {
        'OPENROUTER_API_KEY': 'test_key',
        'OPENROUTER_MODEL': 'test_model',
        'TRADING_MODE': 'simulation'
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars

@pytest.fixture
def parser():
    return Parser()

@pytest.fixture
def transformer(parser):
    return Transformer(parser)

# Test Environment Configuration
class TestEnvironmentSetup:
    def test_env_variables_loaded(self, mock_env_vars):
        assert os.getenv('OPENROUTER_API_KEY') == 'test_key'
        assert os.getenv('OPENROUTER_MODEL') == 'test_model'
        assert os.getenv('TRADING_MODE') == 'simulation'

    def test_pythonpath_configuration(self):
        assert '/workspaces/quantum_cryptocurrency/trading-platform/symbolic_trading' in os.getenv('PYTHONPATH', '')

# Test OpenRouter Integration
class TestOpenRouterIntegration:
    def test_api_connection(self, mock_openrouter):
        mock_openrouter.generate_response.return_value = "Test response"
        assert mock_openrouter.generate_response._mock_return_value == "Test response"

    def test_model_selection(self, mock_env_vars):
        assert os.getenv('OPENROUTER_MODEL') == 'test_model'

    @pytest.mark.asyncio
    async def test_async_response_generation(self, mock_openrouter):
        mock_openrouter.generate_response.return_value = "Async test response"
        response = await mock_openrouter.generate_response("Test prompt")
        assert response == "Async test response"

# Test Mathematical Operations
class TestMathOperations:
    def test_expression_parsing(self, parser):
        expr = "x + 2"
        ast = parser.parse_expression(expr)
        assert isinstance(ast, OperatorNode)
        assert ast.operator == '+'
        assert isinstance(ast.left, VariableNode)
        assert isinstance(ast.right, ConstantNode)

    def test_simplification(self, transformer):
        expr = "x + 0"
        result = transformer.simplify_expression(expr)
        assert result == "x"

    def test_differentiation(self, transformer):
        expr = "x^2"
        result = transformer.differentiate_expression(expr)
        assert "2.0" in result and "x" in result

    def test_integration(self, transformer):
        expr = "2*x"
        result = transformer.integrate_expression(expr)
        assert "x ^ 2.0" in result

    def test_factorization(self, transformer):
        expr = "x^2 + 2*x + 1"
        result = transformer.factor_expression(expr)
        assert "(x + 1)**2" in result

# Test Trading Integration
class TestTradingIntegration:
    def test_simulation_mode(self, mock_env_vars):
        assert os.getenv('TRADING_MODE') == 'simulation'

    @pytest.mark.parametrize("trading_mode", ["simulation", "live", "backtest", "development"])
    def test_trading_modes(self, trading_mode, mock_env_vars):
        with patch.dict(os.environ, {'TRADING_MODE': trading_mode}):
            assert os.getenv('TRADING_MODE') == trading_mode

    def test_trading_safety_checks(self):
        with pytest.raises(ValueError):
            with patch.dict(os.environ, {'TRADING_MODE': 'live', 'SAFETY_CHECKS': 'false'}):
                raise ValueError("Live trading without safety checks")

# Test Expression Tree
class TestExpressionTree:
    def test_constant_node(self):
        node = ConstantNode(5)
        assert node.value == 5
        assert node.evaluate() == 5

    def test_variable_node(self):
        node = VariableNode('x')
        assert node.name == 'x'
        assert node.evaluate({'x': 10}) == 10

    def test_operator_node(self):
        left = ConstantNode(5)
        right = ConstantNode(3)
        node = OperatorNode('+', left, right)
        assert node.evaluate() == 8

    def test_complex_expression(self):
        # (2 * x + 1)
        expr = OperatorNode(
            '+',
            OperatorNode('*', ConstantNode(2), VariableNode('x')),
            ConstantNode(1)
        )
        assert expr.evaluate({'x': 3}) == 7

# Test Error Handling
class TestErrorHandling:
    def test_invalid_expression(self, parser):
        with pytest.raises(SyntaxError):
            parser.parse_expression("x +* 2")

    def test_undefined_variable(self):
        node = VariableNode('x')
        with pytest.raises(KeyError):
            node.evaluate()

    def test_division_by_zero(self):
        expr = OperatorNode('/', ConstantNode(1), ConstantNode(0))
        with pytest.raises(ZeroDivisionError):
            expr.evaluate()

# Test Integration Scenarios
class TestIntegrationScenarios:
    def test_full_expression_workflow(self, transformer):
        expr = "x^2 + 2*x + 1"
        simplified = transformer.simplify_expression(expr)
        derivative = transformer.differentiate_expression(simplified)
        factored = transformer.factor_expression(derivative)
        assert all(term in factored for term in ['x', '2'])

    def test_openrouter_math_integration(self, transformer, mock_openrouter):
        expr = "x^2 + 2*x + 1"
        result = transformer.simplify_expression(expr)
        mock_openrouter.generate_response.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_trading_workflow(self, mock_openrouter, mock_env_vars):
        trader = Trader()
        analysis = await trader.analyze_expression("x^2 + 2*x + 1")
        assert isinstance(analysis, dict)
        assert 'mathematical_analysis' in analysis
        assert 'llm_analysis' in analysis
        assert 'trading_signals' in analysis

# Test Security
class TestSecurity:
    def test_api_key_protection(self, mock_env_vars):
        assert os.getenv('OPENROUTER_API_KEY') is not None
        assert os.getenv('OPENROUTER_API_KEY') != ''

    def test_trading_mode_validation(self):
        with pytest.raises(ValueError):
            with patch.dict(os.environ, {'TRADING_MODE': 'invalid_mode'}):
                raise ValueError("Invalid trading mode")

    def test_expression_sanitization(self, parser):
        with pytest.raises(SyntaxError):
            parser.parse_expression("__import__('os').system('ls')")
