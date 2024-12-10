#!/bin/bash

# Get script directory for relative paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${GREEN}${BOLD}Setting up Virtual Environment${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv "$PROJECT_ROOT/venv"
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source "$PROJECT_ROOT/venv/bin/activate"

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r "$PROJECT_ROOT/requirements.txt"

echo -e "${GREEN}${BOLD}✓ Virtual environment setup complete!${NC}"
