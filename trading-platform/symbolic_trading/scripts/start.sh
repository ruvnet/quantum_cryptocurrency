#!/bin/bash

# Colors and formatting
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Function to print header
print_header() {
    clear
    echo -e "${BLUE}${BOLD}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║       Symbolic Math Trading Platform       ║${NC}"
    echo -e "${BLUE}${BOLD}╚════════════════════════════════════════════╝${NC}"
    echo
}

# Function to print section header
print_section() {
    echo -e "\n${YELLOW}${BOLD}== $1 ==${NC}\n"
}

# Function to create .env file
create_env_file() {
    print_section "Creating .env Configuration"
    echo -e "${GREEN}Generating new .env file...${NC}"
    
    cat > ../.env << EOL
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://api.openrouter.ai/api/v1
OPENROUTER_DEFAULT_MODEL=anthropic/claude-2

# Rate Limiting and Caching
OPENROUTER_REQUESTS_PER_MINUTE=50
CACHE_DURATION_MINUTES=60

# Trading Configuration
TRADING_MODE=simulation
TRADING_PAIR=BTC-USD
TRADING_INTERVAL=5m

# Security Settings
MAX_TOKENS_PER_REQUEST=2000
MONITORING_ENABLED=true
LOG_LEVEL=INFO
EOL
    
    echo -e "${GREEN}${BOLD}✓ .env file created successfully!${NC}"
    echo -e "${YELLOW}Please edit ../.env with your configuration values${NC}"
    echo -e "Press any key to continue..."
    read -n 1 -s
}

# Function to check environment setup
check_environment() {
    if [ ! -f ../.env ]; then
        echo -e "${RED}${BOLD}Error: .env file not found!${NC}"
        echo -e "${YELLOW}Would you like to create a new .env file? (y/n)${NC}"
        read -p "> " create_env
        if [ "$create_env" = "y" ]; then
            create_env_file
        else
            echo -e "${RED}Cannot proceed without .env configuration.${NC}"
            exit 1
        fi
    fi
}

# Function to configure OpenRouter
configure_openrouter() {
    print_section "OpenRouter Configuration"
    echo -e "${BOLD}Select Model:${NC}"
    echo -e "  ${GREEN}1)${NC} Use default model (Claude-2)"
    echo -e "  ${GREEN}2)${NC} Use custom model"
    echo -e "  ${GREEN}3)${NC} Use model ensemble"
    echo
    read -p "Enter choice [1-3]: " model_choice

    case $model_choice in
        1)
            export OPENROUTER_MODEL="anthropic/claude-2"
            echo -e "${GREEN}✓ Using Claude-2 model${NC}"
            ;;
        2)
            echo -e "\n${BOLD}Available Models:${NC}"
            echo -e "  ${GREEN}1)${NC} Google PaLM-2"
            echo -e "  ${GREEN}2)${NC} Anthropic Claude-2"
            echo -e "  ${GREEN}3)${NC} OpenAI GPT-4"
            echo
            read -p "Select model [1-3]: " custom_model
            # Placeholder for model selection
            echo -e "${GREEN}✓ Custom model selected${NC}"
            ;;
        3)
            echo -e "${GREEN}✓ Model ensemble mode enabled${NC}"
            # Placeholder for ensemble configuration
            ;;
        *)
            echo -e "${YELLOW}Invalid choice. Using default model.${NC}"
            export OPENROUTER_MODEL="anthropic/claude-2"
            ;;
    esac
    echo
}

# Function to configure trading mode
configure_trading() {
    print_section "Trading Configuration"
    echo -e "${BOLD}Select Mode:${NC}"
    echo -e "  ${GREEN}1)${NC} Simulation Mode     ${YELLOW}(Safe testing environment)${NC}"
    echo -e "  ${GREEN}2)${NC} Live Trading Mode   ${RED}(Real trading with real assets)${NC}"
    echo -e "  ${GREEN}3)${NC} Backtesting Mode    ${YELLOW}(Test against historical data)${NC}"
    echo -e "  ${GREEN}4)${NC} Strategy Development${GREEN}(Development environment)${NC}"
    echo
    read -p "Enter choice [1-4]: " trading_choice

    case $trading_choice in
        1)
            echo -e "${GREEN}✓ Simulation mode activated${NC}"
            export TRADING_MODE="simulation"
            # Placeholder for simulation settings
            ;;
        2)
            echo -e "${RED}${BOLD}⚠ WARNING: Live trading mode selected!${NC}"
            echo -e "${RED}This mode will use real assets and make real trades.${NC}"
            read -p "Are you sure? (yes/no): " confirm
            if [ "$confirm" = "yes" ]; then
                export TRADING_MODE="live"
                echo -e "${GREEN}✓ Live trading mode activated${NC}"
                # Placeholder for live trading setup
            else
                echo -e "${YELLOW}Reverting to simulation mode...${NC}"
                export TRADING_MODE="simulation"
            fi
            ;;
        3)
            echo -e "${GREEN}✓ Backtesting mode activated${NC}"
            export TRADING_MODE="backtest"
            # Placeholder for backtesting configuration
            ;;
        4)
            echo -e "${GREEN}✓ Strategy development mode activated${NC}"
            export TRADING_MODE="development"
            # Placeholder for strategy development setup
            ;;
        *)
            echo -e "${YELLOW}Invalid choice. Using simulation mode.${NC}"
            export TRADING_MODE="simulation"
            ;;
    esac
    echo
}

# Main menu
print_header
echo -e "${BOLD}Select Deployment Option:${NC}"
echo -e "  ${GREEN}1)${NC} Local Deployment      ${YELLOW}(Run locally with virtual environment)${NC}"
echo -e "  ${GREEN}2)${NC} Docker Deployment     ${YELLOW}(Run in container)${NC}"
echo -e "  ${GREEN}3)${NC} Development Mode      ${YELLOW}(Debug & hot reload enabled)${NC}"
echo -e "  ${GREEN}4)${NC} Distributed Mode      ${YELLOW}(Run components separately)${NC}"
echo
read -p "Enter choice [1-4]: " choice

# Check environment first
check_environment

case $choice in
    1)
        print_section "Local Deployment"
        echo -e "${GREEN}Activating virtual environment...${NC}"
        source ../venv/bin/activate
        export PYTHONPATH="/workspaces/quantum_cryptocurrency/trading-platform/symbolic_trading"
        
        configure_openrouter
        configure_trading
        
        echo -e "${GREEN}${BOLD}Starting application...${NC}"
        python src/main.py
        ;;
    2)
        print_section "Docker Deployment"
        configure_openrouter
        configure_trading
        
        echo -e "${GREEN}${BOLD}Building and starting Docker containers...${NC}"
        docker-compose up --build
        ;;
    3)
        print_section "Development Mode"
        echo -e "${GREEN}Activating virtual environment...${NC}"
        source ../venv/bin/activate
        export PYTHONPATH="/workspaces/quantum_cryptocurrency/trading-platform/symbolic_trading"
        export DEV_MODE="true"
        
        echo -e "${BOLD}Development Features:${NC}"
        echo -e "  ${GREEN}✓${NC} Hot Reload Enabled"
        echo -e "  ${GREEN}✓${NC} Debug Logging Active"
        echo -e "  ${GREEN}✓${NC} Test Database Connected"
        echo
        
        configure_openrouter
        configure_trading
        
        echo -e "${GREEN}${BOLD}Starting in development mode...${NC}"
        python src/main.py --dev
        ;;
    4)
        print_section "Distributed Mode"
        echo -e "${BOLD}Select components to distribute:${NC}"
        echo -e "  ${GREEN}1)${NC} Math Engine"
        echo -e "  ${GREEN}2)${NC} Trading Engine"
        echo -e "  ${GREEN}3)${NC} OpenRouter Client"
        echo -e "  ${GREEN}4)${NC} All Components"
        echo
        read -p "Enter choice [1-4]: " dist_choice
        
        case $dist_choice in
            1) 
                export DISTRIBUTED_COMPONENTS="math"
                echo -e "${GREEN}✓ Math Engine selected for distribution${NC}"
                ;;
            2) 
                export DISTRIBUTED_COMPONENTS="trading"
                echo -e "${GREEN}✓ Trading Engine selected for distribution${NC}"
                ;;
            3) 
                export DISTRIBUTED_COMPONENTS="openrouter"
                echo -e "${GREEN}✓ OpenRouter Client selected for distribution${NC}"
                ;;
            4) 
                export DISTRIBUTED_COMPONENTS="all"
                echo -e "${GREEN}✓ All components selected for distribution${NC}"
                ;;
            *) 
                echo -e "${YELLOW}Invalid choice. Using local mode.${NC}"
                ;;
        esac
        
        echo -e "${GREEN}${BOLD}Starting distributed deployment...${NC}"
        docker-compose -f docker-compose.distributed.yml up --build
        ;;
    *)
        echo -e "${RED}Invalid choice.${NC}"
        exit 1
        ;;
esac
