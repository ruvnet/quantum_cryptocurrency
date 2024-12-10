import numpy as np
from typing import List, Dict

class PerformanceMetrics:
    """Calculate and track trading performance metrics"""
    
    def calculate_mape(self, actual: List[float], predicted: List[float]) -> float:
        """
        Calculate Mean Absolute Percentage Error
        
        Args:
            actual: List of actual values
            predicted: List of predicted values
            
        Returns:
            float: MAPE value
        """
        actual = np.array(actual)
        predicted = np.array(predicted)
        
        # Avoid division by zero
        mask = actual != 0
        return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask]))
        
    def calculate_rmse(self, actual: List[float], predicted: List[float]) -> float:
        """
        Calculate Root Mean Square Error
        
        Args:
            actual: List of actual values
            predicted: List of predicted values
            
        Returns:
            float: RMSE value
        """
        actual = np.array(actual)
        predicted = np.array(predicted)
        
        return np.sqrt(np.mean((actual - predicted) ** 2))
        
    def calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float) -> float:
        """
        Calculate Sharpe Ratio
        
        Args:
            returns: List of period returns
            risk_free_rate: Risk-free rate (annualized)
            
        Returns:
            float: Sharpe ratio
        """
        returns = np.array(returns)
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        
        if len(returns) == 0 or np.std(returns) == 0:
            return 0
            
        return np.sqrt(252) * np.mean(excess_returns) / np.std(returns)
        
    def calculate_prediction_accuracy(self, actual: List[float], predicted: List[float],
                                   threshold: float = 0.02) -> float:
        """
        Calculate prediction accuracy within threshold
        
        Args:
            actual: List of actual values
            predicted: List of predicted values
            threshold: Acceptable error threshold (default 2%)
            
        Returns:
            float: Accuracy score (0-1)
        """
        actual = np.array(actual)
        predicted = np.array(predicted)
        
        errors = np.abs((actual - predicted) / actual)
        accurate_predictions = np.sum(errors <= threshold)
        
        return accurate_predictions / len(actual)
        
    def calculate_roi(self, initial_investment: float, final_value: float,
                     time_period_days: int) -> float:
        """
        Calculate Return on Investment
        
        Args:
            initial_investment: Initial investment amount
            final_value: Final portfolio value
            time_period_days: Number of days
            
        Returns:
            float: ROI as decimal
        """
        return (final_value - initial_investment) / initial_investment
        
    def compare_strategy_performance(self, bot_returns: List[float],
                                   market_returns: List[float]) -> Dict[str, float]:
        """
        Compare strategy performance against market
        
        Args:
            bot_returns: List of strategy returns
            market_returns: List of market returns
            
        Returns:
            Dict containing performance metrics
        """
        bot_returns = np.array(bot_returns)
        market_returns = np.array(market_returns)
        
        # Calculate beta (market sensitivity)
        covariance = np.cov(bot_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        beta = covariance / market_variance if market_variance != 0 else 1
        
        # Calculate alpha (excess return)
        alpha = np.mean(bot_returns) - beta * np.mean(market_returns)
        
        # Calculate Sharpe ratio
        risk_free_rate = 0.02  # Assume 2% annual risk-free rate
        sharpe = self.calculate_sharpe_ratio(bot_returns, risk_free_rate)
        
        # Calculate maximum drawdown
        cumulative_returns = np.cumprod(1 + bot_returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdowns = (running_max - cumulative_returns) / running_max
        max_drawdown = np.max(drawdowns)
        
        return {
            "alpha": alpha,
            "beta": beta,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_drawdown,
            "total_return": np.prod(1 + bot_returns) - 1,
            "volatility": np.std(bot_returns) * np.sqrt(252),  # Annualized
            "market_correlation": np.corrcoef(bot_returns, market_returns)[0][1]
        }
