#!/bin/bash

# Colors and formatting
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Function to print header
print_header() {
    clear
    echo -e "${BLUE}${BOLD}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║       Symbolic Math Testing Suite          ║${NC}"
    echo -e "${BLUE}${BOLD}╚════════════════════════════════════════════╝${NC}"
    echo
}

# Function to run tests
run_tests() {
    local test_type=$1
    local coverage_flag=$2
    
    export PYTHONPATH="$PROJECT_ROOT"
    
    case $test_type in
        "all")
            echo -e "\n${YELLOW}${BOLD}== Running All Tests ==${NC}\n"
            if [ "$coverage_flag" = "true" ]; then
                pytest "$PROJECT_ROOT/tests" -v --cov="$PROJECT_ROOT/src" --cov-report=term-missing
            else
                pytest "$PROJECT_ROOT/tests" -v
            fi
            ;;
        "unit")
            echo -e "\n${YELLOW}${BOLD}== Running Unit Tests ==${NC}\n"
            pytest "$PROJECT_ROOT/tests" -v -m "not integration and not performance and not security"
            ;;
        "integration")
            echo -e "\n${YELLOW}${BOLD}== Running Integration Tests ==${NC}\n"
            pytest "$PROJECT_ROOT/tests" -v -m "integration"
            ;;
        "performance")
            echo -e "\n${YELLOW}${BOLD}== Running Performance Tests ==${NC}\n"
            pytest "$PROJECT_ROOT/tests" -v -m "performance"
            ;;
        "security")
            echo -e "\n${YELLOW}${BOLD}== Running Security Tests ==${NC}\n"
            pytest "$PROJECT_ROOT/tests" -v -m "security"
            ;;
        *)
            echo -e "${RED}Invalid test type${NC}"
            return 1
            ;;
    esac
}

# Main menu
while true; do
    print_header
    echo -e "${BOLD}Select Test Suite:${NC}"
    echo "  1) Run All Tests"
    echo "  2) Run Unit Tests Only"
    echo "  3) Run Integration Tests"
    echo "  4) Run Performance Tests"
    echo "  5) Run Security Tests"
    echo "  6) Generate Coverage Report"
    echo "  7) Run Specific Test File"
    echo "  8) Exit"
    echo
    read -p "Enter choice [1-8]: " choice
    
    case $choice in
        1)
            run_tests "all" "false"
            ;;
        2)
            run_tests "unit" "false"
            ;;
        3)
            run_tests "integration" "false"
            ;;
        4)
            run_tests "performance" "false"
            ;;
        5)
            run_tests "security" "false"
            ;;
        6)
            run_tests "all" "true"
            ;;
        7)
            echo
            read -p "Enter test file path (relative to tests/): " test_file
            export PYTHONPATH="$PROJECT_ROOT"
            pytest "$PROJECT_ROOT/tests/$test_file" -v
            ;;
        8)
            echo -e "\n${GREEN}Exiting test suite. Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}Invalid choice. Please try again.${NC}"
            ;;
    esac
    
    echo
    read -p "Press Enter to continue..."
done
