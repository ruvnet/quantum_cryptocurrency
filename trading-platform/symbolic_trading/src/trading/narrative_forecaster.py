from src.llm_integration.openrouter_client import OpenRouterClient
import numpy as np
from typing import Dict, List, Any
import re

class NarrativeForecaster:
    """Narrative-based price forecasting using LLM"""
    
    def __init__(self):
        """Initialize forecaster with OpenRouter client"""
        self.llm_client = OpenRouterClient()
        
    async def generate_narrative(self, symbol: str, current_price: float,
                               volume: float, support_level: float,
                               resistance_level: float) -> Dict[str, Any]:
        """Generate future retrospective narrative"""
        prompt = self._construct_future_prompt(
            symbol, current_price, volume, support_level, resistance_level
        )
        
        response = await self.llm_client.generate_response(prompt)
        
        return {
            "narrative": response["narrative"],
            "price_prediction": response["price_prediction"],
            "confidence_score": response["confidence_score"]
        }
        
    def _construct_future_prompt(self, symbol: str, current_price: float,
                               volume: float, support_level: float,
                               resistance_level: float) -> str:
        """Construct future retrospective prompt"""
        return f"""Looking back from tomorrow, describe what happened to {symbol} 
        given these current conditions:
        - Current Price: ${current_price:,.2f}
        - 24h Volume: {volume:,.2f}
        - Support Level: ${support_level:,.2f}
        - Resistance Level: ${resistance_level:,.2f}

        Frame your response as a retrospective analysis, explaining:
        1. What price movements occurred
        2. What factors drove these movements
        3. How trading volume changed
        4. Which technical levels were tested
        
        End with a specific price prediction and confidence score (0-1).
        """
        
    def extract_key_factors(self, narrative: str) -> List[str]:
        """Extract key driving factors from narrative"""
        # Common market factors to look for
        factors = [
            "institutional adoption",
            "regulatory news",
            "market sentiment",
            "technical levels",
            "trading volume",
            "support level",
            "resistance level",
            "market momentum"
        ]
        
        found_factors = []
        for factor in factors:
            if factor.lower() in narrative.lower():
                found_factors.append(factor)
                
        return found_factors
        
    def calculate_sentiment_score(self, narrative: str) -> float:
        """Calculate sentiment score from narrative"""
        positive_words = [
            "bullish", "increase", "gain", "positive", "growth",
            "support", "strong", "confidence", "adoption", "momentum"
        ]
        
        negative_words = [
            "bearish", "decrease", "loss", "negative", "decline",
            "resistance", "weak", "uncertainty", "rejection", "selling"
        ]
        
        # Count word occurrences
        positive_count = sum(narrative.lower().count(word) for word in positive_words)
        negative_count = sum(narrative.lower().count(word) for word in negative_words)
        
        total_count = positive_count + negative_count
        if total_count == 0:
            return 0.5
            
        return positive_count / total_count
        
    def adjust_profit_threshold(self, base_threshold: float, confidence_score: float,
                              sentiment_score: float, volatility: float) -> float:
        """Dynamically adjust profit threshold based on analysis"""
        # Start with base threshold
        adjusted_threshold = base_threshold
        
        # Adjust based on confidence
        confidence_factor = (confidence_score - 0.5) * 2  # Scale to [-1, 1]
        adjusted_threshold *= (1 + confidence_factor * 0.2)  # ±20% adjustment
        
        # Adjust based on sentiment
        sentiment_factor = (sentiment_score - 0.5) * 2  # Scale to [-1, 1]
        adjusted_threshold *= (1 + sentiment_factor * 0.15)  # ±15% adjustment
        
        # Adjust based on volatility
        volatility_factor = volatility / 0.02  # Normalize to typical volatility
        adjusted_threshold *= (1 + (volatility_factor - 1) * 0.1)  # ±10% adjustment
        
        # Ensure threshold stays within reasonable bounds
        min_threshold = base_threshold * 0.5
        max_threshold = base_threshold * 2.0
        return np.clip(adjusted_threshold, min_threshold, max_threshold)
