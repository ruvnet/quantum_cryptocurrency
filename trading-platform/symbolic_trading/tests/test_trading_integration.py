import pytest
from unittest.mock import Mock, patch
from src.trading.trader import Trader
from src.trading.crypto_api import CryptoAPI
from src.trading.performance_metrics import PerformanceMetrics
import asyncio

@pytest.fixture
def trader():
    return Trader()

@pytest.fixture
def crypto_api():
    return CryptoAPI()

@pytest.fixture
def performance_metrics():
    return PerformanceMetrics()

class TestLiveTrading:
    @pytest.mark.asyncio
    async def test_simulation_trade_execution(self, trader):
        """Test simulation trading execution"""
        trade_params = {
            'symbol': 'BTC-USD',
            'amount': 0.1,
            'price': 50000.0,
            'type': 'market'
        }

        # Set to simulation mode
        trader.mode = 'simulation'
            
        # Execute trade
        result = await trader.execute_trade(trade_params)
            
        assert result['status'] == 'simulated'
        assert result['result'] == 'success'
        assert result['params'] == trade_params

    @pytest.mark.asyncio
    async def test_live_trade_validation(self, trader):
        """Test trade validation in live mode"""
        # Invalid trade params
        invalid_params = {
            'symbol': 'BTC-USD',
            # Missing required params
        }

        # Set to live mode
        trader.mode = 'live'
        
        # Should fail validation
        assert not trader.validate_trade(invalid_params)

        # Valid trade params
        valid_params = {
            'symbol': 'BTC-USD',
            'amount': 0.1,
            'price': 50000.0,
            'type': 'market'
        }
        
        # Should pass validation
        assert trader.validate_trade(valid_params)

    @pytest.mark.asyncio
    async def test_live_trade_not_implemented(self, trader):
        """Test that live trading raises NotImplementedError"""
        trade_params = {
            'symbol': 'BTC-USD',
            'amount': 0.1,
            'price': 50000.0,
            'type': 'market'
        }

        # Set to live mode
        trader.mode = 'live'
        
        # Should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            await trader.execute_trade(trade_params)

class TestTradingSignals:
    @pytest.mark.asyncio
    async def test_signal_generation(self, trader):
        """Test trading signal generation from analysis"""
        expression = "x^2 + 2*x"
        
        # Mock LLM analysis
        mock_llm_response = {
            'sentiment': 'bullish',
            'confidence': 0.8,
            'reasoning': 'Increasing momentum'
        }

        # Patch LLM client
        with patch('src.llm_integration.openrouter_client.OpenRouterClient.analyze_expression',
                  return_value=mock_llm_response):
            analysis = await trader.analyze_expression(expression)
            signals = trader._extract_trading_signals(
                analysis['mathematical_analysis'],
                analysis['llm_analysis']
            )
            
            assert 'signal' in signals
            assert 'confidence' in signals
            assert 'recommendation' in signals
            assert signals['confidence'] > 0

class TestPerformanceMetrics:
    def test_calculate_sharpe_ratio(self, performance_metrics):
        """Test Sharpe ratio calculation"""
        returns = [0.02, -0.01, 0.03, 0.01, -0.02]
        risk_free_rate = 0.01
        
        sharpe = performance_metrics.calculate_sharpe_ratio(returns, risk_free_rate)
        assert isinstance(sharpe, float)
        assert sharpe != 0  # Should not be placeholder value

    def test_calculate_prediction_accuracy(self, performance_metrics):
        """Test prediction accuracy calculation"""
        actual = [100, 105, 95, 110]
        predicted = [102, 103, 96, 108]
        
        accuracy = performance_metrics.calculate_prediction_accuracy(actual, predicted)
        assert isinstance(accuracy, float)
        assert 0 <= accuracy <= 1

    def test_calculate_roi(self, performance_metrics):
        """Test ROI calculation"""
        initial_investment = 10000
        final_value = 12000
        time_period_days = 30
        
        roi = performance_metrics.calculate_roi(initial_investment, final_value, time_period_days)
        assert roi == 0.2  # 20% ROI

class TestCryptoAPI:
    @pytest.mark.asyncio
    async def test_market_order(self, crypto_api):
        """Test market order execution"""
        order_params = {
            'instrument_name': 'BTC-USD',
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': 0.1
        }
        
        # Mock exchange response
        mock_response = {
            'result': {
                'order_id': '12345',
                'status': 'filled',
                'filled': 0.1,
                'average': 50000.0
            }
        }
        
        with patch('src.trading.crypto_api.CryptoAPI._request',
                  return_value=mock_response):
            result = await crypto_api.place_order(
                order_params['instrument_name'],
                order_params['side'],
                order_params['quantity'],
                None  # Market order, no price
            )
            
            assert result['order_id'] == '12345'
            assert result['status'] == 'filled'

    @pytest.mark.asyncio
    async def test_limit_order(self, crypto_api):
        """Test limit order execution"""
        order_params = {
            'instrument_name': 'BTC-USD',
            'side': 'BUY',
            'type': 'LIMIT',
            'quantity': 0.1,
            'price': 50000.0
        }
        
        # Mock exchange response
        mock_response = {
            'result': {
                'order_id': '12345',
                'status': 'open',
                'price': 50000.0
            }
        }
        
        with patch('src.trading.crypto_api.CryptoAPI._request',
                  return_value=mock_response):
            result = await crypto_api.place_order(
                order_params['instrument_name'],
                order_params['side'],
                order_params['quantity'],
                order_params['price']
            )
            
            assert result['order_id'] == '12345'
            assert result['status'] == 'open'
            assert result['price'] == 50000.0

    @pytest.mark.asyncio
    async def test_order_status(self, crypto_api):
        """Test order status checking"""
        order_id = '12345'
        
        # Mock exchange response
        mock_response = {
            'result': {
                'order_id': order_id,
                'status': 'filled',
                'filled': 0.1,
                'remaining': 0
            }
        }
        
        with patch('src.trading.crypto_api.CryptoAPI._request',
                  return_value=mock_response):
            result = await crypto_api.get_order_status(order_id)
            
            assert result['order_id'] == order_id
            assert result['status'] == 'filled'
            assert result['remaining'] == 0
