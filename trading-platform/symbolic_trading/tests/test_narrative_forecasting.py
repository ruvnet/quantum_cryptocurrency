import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.trading.narrative_forecaster import NarrativeForecaster
from src.trading.performance_metrics import PerformanceMetrics
import numpy as np

@pytest.fixture
def mock_llm_response():
    return {
        "narrative": """
        Looking back from tomorrow, we can see that BTC experienced a significant uptick 
        due to increased institutional adoption and positive regulatory news. The key 
        support level at $48,000 held strong, leading to a push toward $52,000. 
        Trading volume increased by 25%, indicating strong buyer conviction.
        """,
        "price_prediction": 52000.0,
        "confidence_score": 0.85
    }

@pytest.fixture
def sample_price_data():
    return {
        "actual_prices": [50000, 51000, 52000, 51500, 52500],
        "predicted_prices": [50200, 51200, 51800, 51800, 52300],
        "timestamps": [
            "2024-01-01", "2024-01-02", "2024-01-03", 
            "2024-01-04", "2024-01-05"
        ]
    }

class TestNarrativeForecasting:
    @pytest.mark.asyncio
    async def test_generate_narrative(self, mock_llm_response):
        """Test narrative generation"""
        with patch('src.llm_integration.openrouter_client.OpenRouterClient.generate_response') as mock_generate:
            mock_generate.return_value = mock_llm_response
            
            forecaster = NarrativeForecaster()
            narrative = await forecaster.generate_narrative(
                symbol="BTC",
                current_price=50000.0,
                volume=1000.0,
                support_level=48000.0,
                resistance_level=53000.0
            )
            
            assert "institutional adoption" in narrative["narrative"]
            assert narrative["price_prediction"] == 52000.0
            assert narrative["confidence_score"] > 0.8
            
    def test_extract_key_factors(self, mock_llm_response):
        """Test extraction of key factors from narrative"""
        forecaster = NarrativeForecaster()
        factors = forecaster.extract_key_factors(mock_llm_response["narrative"])
        
        assert "institutional adoption" in factors
        assert "regulatory news" in factors
        assert "support level" in factors
        assert "trading volume" in factors
        
    def test_calculate_sentiment_score(self, mock_llm_response):
        """Test sentiment score calculation"""
        forecaster = NarrativeForecaster()
        sentiment_score = forecaster.calculate_sentiment_score(
            mock_llm_response["narrative"]
        )
        
        assert 0 <= sentiment_score <= 1
        assert sentiment_score > 0.5  # Positive sentiment in mock response
        
    def test_adjust_profit_threshold(self):
        """Test dynamic profit threshold adjustment"""
        forecaster = NarrativeForecaster()
        base_threshold = 0.05  # 5% profit target
        
        # Test with high confidence and positive sentiment
        adjusted_threshold = forecaster.adjust_profit_threshold(
            base_threshold=base_threshold,
            confidence_score=0.85,
            sentiment_score=0.8,
            volatility=0.02
        )
        assert adjusted_threshold > base_threshold
        
        # Test with low confidence and negative sentiment
        adjusted_threshold = forecaster.adjust_profit_threshold(
            base_threshold=base_threshold,
            confidence_score=0.3,
            sentiment_score=0.2,
            volatility=0.02
        )
        assert adjusted_threshold < base_threshold

class TestPerformanceMetrics:
    def test_calculate_mape(self, sample_price_data):
        """Test Mean Absolute Percentage Error calculation"""
        metrics = PerformanceMetrics()
        mape = metrics.calculate_mape(
            actual=sample_price_data["actual_prices"],
            predicted=sample_price_data["predicted_prices"]
        )
        assert isinstance(mape, float)
        assert mape < 0.05  # Less than 5% error
        
    def test_calculate_rmse(self, sample_price_data):
        """Test Root Mean Square Error calculation"""
        metrics = PerformanceMetrics()
        rmse = metrics.calculate_rmse(
            actual=sample_price_data["actual_prices"],
            predicted=sample_price_data["predicted_prices"]
        )
        assert isinstance(rmse, float)
        assert rmse < 1000  # Reasonable error range for BTC prices
        
    def test_calculate_sharpe_ratio(self):
        """Test Sharpe Ratio calculation"""
        metrics = PerformanceMetrics()
        returns = [0.02, -0.01, 0.03, 0.01, -0.02]  # Daily returns
        risk_free_rate = 0.02  # 2% annual risk-free rate
        
        sharpe = metrics.calculate_sharpe_ratio(
            returns=returns,
            risk_free_rate=risk_free_rate
        )
        assert isinstance(sharpe, float)
        
    def test_calculate_prediction_accuracy(self, sample_price_data):
        """Test prediction accuracy calculation"""
        metrics = PerformanceMetrics()
        accuracy = metrics.calculate_prediction_accuracy(
            actual=sample_price_data["actual_prices"],
            predicted=sample_price_data["predicted_prices"],
            threshold=0.02  # 2% tolerance
        )
        assert 0 <= accuracy <= 1
        
    def test_calculate_roi(self):
        """Test ROI calculation"""
        metrics = PerformanceMetrics()
        initial_investment = 10000
        final_value = 13800
        days = 30
        
        roi = metrics.calculate_roi(
            initial_investment=initial_investment,
            final_value=final_value,
            time_period_days=days
        )
        assert roi == 0.38  # 38% ROI
        
    def test_compare_strategy_performance(self):
        """Test strategy performance comparison"""
        metrics = PerformanceMetrics()
        bot_returns = [0.02, -0.01, 0.03, 0.01, -0.02]
        market_returns = [0.01, -0.02, 0.02, 0.01, -0.01]
        
        comparison = metrics.compare_strategy_performance(
            bot_returns=bot_returns,
            market_returns=market_returns
        )
        
        assert "alpha" in comparison
        assert "beta" in comparison
        assert "sharpe_ratio" in comparison
        assert "max_drawdown" in comparison
