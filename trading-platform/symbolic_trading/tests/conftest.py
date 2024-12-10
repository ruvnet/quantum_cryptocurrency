import pytest
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "benchmark: mark test as a performance benchmark"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as a security test"
    )

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    test_env = {
        'PYTHONPATH': project_root,
        'TESTING': 'true',
        'OPENROUTER_API_KEY': 'test_key',
        'OPENROUTER_MODEL': 'test_model',
        'TRADING_MODE': 'simulation',
        'LOG_LEVEL': 'DEBUG'
    }
    with pytest.MonkeyPatch.context() as mp:
        for key, value in test_env.items():
            mp.setenv(key, value)
        yield

@pytest.fixture
def sample_expressions():
    """Provide sample mathematical expressions for testing."""
    return {
        'simple': 'x + 2',
        'quadratic': 'x^2 + 2*x + 1',
        'complex': '(x^2 + 2*x + 1)/(x - 1)',
        'trigonometric': 'sin(x) + cos(x)',
        'exponential': 'e^x + ln(x)',
        'invalid': 'x +* 2'
    }

@pytest.fixture
def sample_variables():
    """Provide sample variable values for testing."""
    return {
        'x': 2,
        'y': 3,
        'z': 4
    }

@pytest.fixture
def mock_openrouter_response():
    """Provide mock responses for OpenRouter API tests."""
    return {
        'market_analysis': {
            'sentiment': 'positive',
            'confidence': 0.85,
            'recommendation': 'buy',
            'reasoning': 'Strong technical indicators and positive market sentiment'
        },
        'expression_analysis': {
            'complexity': 'medium',
            'suggested_simplification': 'Combine like terms',
            'mathematical_insight': 'Expression shows quadratic growth pattern'
        },
        'error_response': {
            'error': 'Rate limit exceeded',
            'retry_after': 60
        }
    }

@pytest.fixture
def mock_trading_data():
    """Provide mock trading data for testing."""
    return {
        'current_price': 50000.00,
        'volume_24h': 1000000,
        'price_change_24h': 2.5,
        'market_cap': 1000000000,
        'trading_pairs': ['BTC-USD', 'ETH-USD', 'XRP-USD'],
        'order_book': {
            'bids': [(49995, 1.5), (49990, 2.0)],
            'asks': [(50005, 1.0), (50010, 2.5)]
        },
        'historical_data': [
            {'timestamp': '2023-01-01', 'price': 49000},
            {'timestamp': '2023-01-02', 'price': 49500},
            {'timestamp': '2023-01-03', 'price': 50000}
        ]
    }

@pytest.fixture
def mock_system_state():
    """Provide mock system state for testing."""
    return {
        'cpu_usage': 45.5,
        'memory_usage': 1024,
        'active_connections': 5,
        'cache_size': 256,
        'last_api_call': '2023-01-01T12:00:00Z',
        'error_count': 0,
        'performance_metrics': {
            'response_time_ms': 150,
            'requests_per_second': 10
        }
    }

@pytest.fixture
def test_logger():
    """Configure test logger."""
    import logging
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
    return logger
