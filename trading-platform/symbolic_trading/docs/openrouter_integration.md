# OpenRouter API Integration Specification

## Overview

This specification outlines the integration of OpenRouter API for enhanced mathematical expression analysis and trading predictions using Large Language Models (LLMs). The integration will complement the existing symbolic mathematics engine with natural language processing capabilities.

## Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://api.openrouter.ai/api/v1
OPENROUTER_DEFAULT_MODEL=anthropic/claude-2

# Rate Limiting and Caching
OPENROUTER_REQUESTS_PER_MINUTE=50
CACHE_DURATION_MINUTES=60

# Backup Model Configuration (Optional)
BACKUP_MODEL=google/palm-2
FALLBACK_TEMPERATURE=0.7

# Security and Monitoring
MAX_TOKENS_PER_REQUEST=2000
MONITORING_ENABLED=true
LOG_LEVEL=INFO
```

## OpenRouter API Integration

### 1. API Client Implementation

Create a new module `src/llm_integration/openrouter_client.py`:

```python
class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = os.getenv('OPENROUTER_BASE_URL')
        self.default_model = os.getenv('OPENROUTER_DEFAULT_MODEL')
        
    async def generate_response(self, prompt, temperature=0.7):
        # Implementation for API calls
        pass
        
    def validate_response(self, response):
        # Response validation logic
        pass
```

### 2. Mathematical Expression Analysis

Enhance the existing symbolic math engine with LLM capabilities:

```python
class EnhancedMathEngine:
    def __init__(self):
        self.symbolic_engine = SymbolicMathEngine()
        self.llm_client = OpenRouterClient()
        
    async def analyze_expression(self, expression):
        # Combine symbolic analysis with LLM insights
        pass
```

## Integration Points

### 1. Expression Optimization
- Use LLM to suggest optimal mathematical transformations
- Enhance simplification strategies with pattern recognition
- Generate human-readable explanations for transformations

### 2. Trading Strategy Enhancement
- Analyze mathematical patterns for trading signals
- Generate narrative predictions for market movements
- Validate mathematical models with LLM reasoning

## Security Considerations

1. API Key Protection:
   - Store API keys in .env file
   - Never commit .env to version control
   - Implement key rotation mechanism

2. Rate Limiting:
   - Implement request throttling
   - Cache frequently used responses
   - Monitor API usage

3. Data Validation:
   - Validate all API responses
   - Sanitize inputs before sending to API
   - Implement timeout mechanisms

## Implementation Steps

1. Environment Setup:
```bash
pip install python-dotenv openai requests aiohttp
```

2. Configuration Loading:
```python
from dotenv import load_dotenv
load_dotenv()
```

3. Integration Testing:
```python
class TestOpenRouterIntegration:
    def test_api_connection(self):
        # Test API connectivity
        pass
        
    def test_response_validation(self):
        # Test response validation
        pass
```

## Usage Examples

### 1. Enhanced Expression Analysis

```python
async def analyze_complex_expression():
    engine = EnhancedMathEngine()
    expression = "3x^2 + 2x + 1"
    
    # Get symbolic analysis
    symbolic_result = engine.symbolic_engine.analyze(expression)
    
    # Enhance with LLM insights
    llm_insights = await engine.llm_client.generate_response(
        f"Analyze the mathematical expression: {expression}"
    )
    
    return {
        "symbolic_analysis": symbolic_result,
        "llm_insights": llm_insights
    }
```

### 2. Trading Strategy Integration

```python
async def generate_trading_strategy(expression, market_data):
    engine = EnhancedMathEngine()
    
    # Combine mathematical analysis with market data
    strategy = await engine.analyze_trading_opportunity(
        expression,
        market_data
    )
    
    return strategy
```

## Error Handling

1. API Errors:
```python
class OpenRouterError(Exception):
    pass

def handle_api_error(error):
    if error.status_code == 429:
        # Handle rate limiting
        pass
    elif error.status_code == 401:
        # Handle authentication errors
        pass
```

2. Fallback Mechanism:
```python
async def fallback_to_backup_model():
    backup_model = os.getenv('BACKUP_MODEL')
    # Implementation
```

## Monitoring and Logging

1. Setup logging configuration:
```python
import logging

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

2. Monitor API usage:
```python
class APIMonitor:
    def track_request(self, endpoint, status):
        # Implementation
    
    def get_usage_statistics(self):
        # Implementation
```

## Performance Considerations

1. Caching Strategy:
- Implement response caching for frequently used expressions
- Cache invalidation based on time or market conditions
- Memory usage monitoring

2. Concurrent Requests:
- Implement connection pooling
- Handle multiple concurrent API calls efficiently
- Manage request queues during high load

## Maintenance and Updates

1. Regular Tasks:
- Monitor API version changes
- Update model selections based on performance
- Rotate API keys periodically
- Review and optimize caching strategy

2. Documentation:
- Keep integration documentation updated
- Document any API changes or new features
- Maintain troubleshooting guides

## Future Enhancements

1. Planned Features:
- Multi-model ensemble analysis
- Advanced caching strategies
- Real-time performance monitoring
- Custom model fine-tuning support

2. Integration Expansion:
- Additional LLM providers
- Enhanced mathematical reasoning
- Automated strategy optimization

## Conclusion

This integration specification provides a framework for enhancing the symbolic math engine with OpenRouter API capabilities. The implementation should follow these guidelines while maintaining flexibility for future improvements and optimizations.
