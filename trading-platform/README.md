# Symbolic Trading Platform

## Transform Your Trading with Advanced Mathematics and AI

The Symbolic Trading Platform is a cutting-edge algorithmic trading solution that combines symbolic mathematics, machine learning, and narrative analysis to give you an edge in cryptocurrency markets.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-green.svg)
![NumPy](https://img.shields.io/badge/numpy-%E2%89%A51.21.0-blue.svg)
![SymPy](https://img.shields.io/badge/sympy-%E2%89%A51.9-blue.svg)
![Docker](https://img.shields.io/badge/docker-%E2%89%A53.8-blue.svg)

## 🚀 Key Features

- **Symbolic Mathematics Engine**
  - Advanced pattern recognition for technical analysis
  - Automated derivative calculations for trend analysis
  - Mathematical optimization of trading strategies
  - Real-time formula transformation and evaluation

- **AI-Powered Narrative Forecasting**
  - Natural language processing of market sentiment
  - Real-time market narrative analysis
  - Predictive modeling using narrative patterns
  - Sentiment-based trading signals

- **Cryptocurrency Integration**
  - Real-time market data integration
  - Automated order execution
  - Multi-exchange support
  - Comprehensive performance metrics

- **LLM Integration**
  - OpenRouter integration for advanced analysis
  - AI-assisted strategy development
  - Natural language trading commands
  - Automated market research

## 🔧 Technical Overview

### Architecture

The platform supports both monolithic and distributed deployments:

#### Monolithic Architecture
```
symbolic_trading/
├── src/
│   ├── transformers/      # Symbolic mathematics engine
│   ├── trading/          # Core trading functionality
│   ├── llm_integration/  # AI/ML components
│   ├── parser/          # Mathematical expression parsing
│   └── utils/           # Shared utilities
```

#### Distributed Architecture
```
Services:
├── math-engine       # Port 8001
│   └── Symbolic mathematics processing
├── trading-engine    # Port 8002
│   └── Trading operations and execution
└── openrouter-client # Port 8003
    └── AI/ML processing and analysis
```

### Core Components

1. **Math Engine (Port 8001)**
   - Expression parsing and transformation
   - Pattern matching and rule systems
   - Differentiation and integration capabilities
   - Mathematical optimization

2. **Trading Engine (Port 8002)**
   - Market data processing
   - Order management
   - Risk assessment
   - Performance tracking

3. **OpenRouter Client (Port 8003)**
   - AI model integration
   - Natural language processing
   - Market narrative analysis
   - Strategy recommendations

### Technology Stack

- **Core Dependencies**
  - Python 3.12+
  - NumPy ≥1.21.0 (Numerical computations)
  - SymPy ≥1.9 (Symbolic mathematics)
  - SQLAlchemy ≥1.4.0 (Database ORM)
  - aiohttp ≥3.8.0 (Async HTTP client)

- **Development Tools**
  - pytest ≥7.0.0 (Testing framework)
  - black ≥21.9b0 (Code formatting)
  - flake8 ≥3.9.0 (Code linting)

- **Infrastructure**
  - Docker ≥3.8
  - Docker Compose
  - Async I/O support
  - Environment-based configuration

## 🚀 Getting Started

### Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install dependencies:
```bash
cd symbolic_trading
pip install -r requirements.txt
```

3. Set up the environment:
```bash
./scripts/setup_venv.sh
```

4. Start the platform:
```bash
./scripts/start.sh
```

### Docker Deployment

#### Monolithic Deployment
1. Configure environment variables in `.env`:
```env
TRADING_MODE=simulation
OPENROUTER_API_KEY=your_api_key
TRADING_PAIR=BTC-USD
TRADING_INTERVAL=5m
LOG_LEVEL=INFO
```

2. Build and run:
```bash
docker-compose up -d
```

#### Distributed Deployment
1. Configure environment variables as above

2. Build and run distributed services:
```bash
docker-compose -f docker-compose.yml -f docker-compose.distributed.yml up -d
```

This will start:
- Math Engine on port 8001
- Trading Engine on port 8002
- OpenRouter Client on port 8003

### Configuration Options

| Environment Variable | Description | Default | Service |
|---------------------|-------------|---------|----------|
| TRADING_MODE | Trading mode (simulation/live) | simulation | All |
| OPENROUTER_API_KEY | OpenRouter API key | required | OpenRouter |
| OPENROUTER_BASE_URL | OpenRouter API base URL | https://api.openrouter.ai/api/v1 | OpenRouter |
| OPENROUTER_DEFAULT_MODEL | Default LLM model | anthropic/claude-2 | OpenRouter |
| TRADING_PAIR | Trading pair to monitor | BTC-USD | Trading |
| TRADING_INTERVAL | Trading interval | 5m | Trading |
| MAX_TOKENS_PER_REQUEST | Max tokens per LLM request | 2000 | OpenRouter |
| MONITORING_ENABLED | Enable monitoring | true | All |
| LOG_LEVEL | Logging level | INFO | All |
| COMPONENT | Service component | N/A | All |

## 📈 Performance

The platform includes comprehensive performance metrics:
- Sharpe Ratio calculation
- RMSE (Root Mean Square Error) analysis
- Prediction accuracy tracking
- ROI monitoring

## 🔒 Security

- Secure API key management
- Trading safety checks
- Input sanitization
- Comprehensive error handling

## 🛠 Development

### Testing
```bash
./scripts/test.sh
```

The test suite includes:
- Unit tests
- Integration tests
- Performance tests
- Security tests

### Code Quality
- Black code formatting
- Flake8 linting
- Pytest coverage reports

### Docker Development

#### Monolithic Development
```bash
docker-compose up --build
```

#### Distributed Development
```bash
docker-compose -f docker-compose.yml -f docker-compose.distributed.yml up --build
```

### Service Endpoints
- Math Engine: http://localhost:8001
- Trading Engine: http://localhost:8002
- OpenRouter Client: http://localhost:8003

## 🤝 Support

- Extensive documentation in `/docs`
- Comprehensive test suite
- Regular updates and maintenance
- Community support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Documentation](docs/)
- [Trading Guide](docs/trading.md)
- [OpenRouter Integration](docs/openrouter_integration.md)

## 📦 Dependencies

### Core Dependencies
- numpy ≥1.21.0
- sympy ≥1.9
- python-dotenv ≥0.19.0
- aiohttp ≥3.8.0
- requests ≥2.26.0
- sqlalchemy ≥1.4.0

### Development Dependencies
- pytest ≥7.0.0 (with asyncio, coverage, and mock plugins)
- black ≥21.9b0
- flake8 ≥3.9.0

### Utilities
- python-dateutil ≥2.8.2
- pytz ≥2021.3
- pyyaml ≥5.4.1

## 🐳 Docker Support

The platform supports flexible deployment options:

### Monolithic Deployment
- Single container deployment
- All components in one service
- Simplified configuration
- Port 8000 for API access

### Distributed Deployment
- Microservices architecture
- Independent scaling of components
- Service-specific configuration
- Load balancing ready
- Inter-service communication
- Bridge network for service discovery

---

*Transform your trading with the power of mathematics and AI*
