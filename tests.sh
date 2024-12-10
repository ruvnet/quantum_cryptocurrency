#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default configuration
VERBOSE=false
COVERAGE=false
FAIL_FAST=false
MAX_FAIL=0
TEST_ENV="development"

# Function to print colored header
print_header() {
    echo -e "${BLUE}================================================"
    echo -e "    Quantum Cryptocurrency Test Runner"
    echo -e "================================================${NC}\n"
}

# Function to print help
print_help() {
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./tests.sh [options]"
    echo
    echo -e "${YELLOW}Options:${NC}"
    echo "  -v, --verbose     Enable verbose output"
    echo "  -c, --coverage    Generate coverage report"
    echo "  -f, --fail-fast   Stop on first failure"
    echo "  -m, --max-fail N  Stop after N failures"
    echo "  -e, --env ENV     Set test environment (development/staging/production)"
    echo "  -h, --help        Show this help message"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -f|--fail-fast)
            FAIL_FAST=true
            shift
            ;;
        -m|--max-fail)
            MAX_FAIL="$2"
            shift 2
            ;;
        -e|--env)
            TEST_ENV="$2"
            shift 2
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# Build pytest command based on options
build_pytest_cmd() {
    local cmd="PYTHONPATH=/workspaces/quantum_cryptocurrency python -m pytest"
    
    if [ "$VERBOSE" = true ]; then
        cmd="$cmd -v"
    fi
    
    if [ "$COVERAGE" = true ]; then
        cmd="$cmd --cov=quantum_crypto --cov-report=term-missing"
    fi
    
    if [ "$FAIL_FAST" = true ]; then
        cmd="$cmd --exitfirst"
    fi
    
    if [ $MAX_FAIL -gt 0 ]; then
        cmd="$cmd --maxfail=$MAX_FAIL"
    fi
    
    echo "$cmd"
}

# Function to run specific test suite
run_test_suite() {
    local suite=$1
    local pytest_cmd=$(build_pytest_cmd)
    
    echo -e "${BLUE}Running $suite tests...${NC}"
    echo -e "${YELLOW}Environment: $TEST_ENV${NC}"
    echo -e "${YELLOW}Command: $pytest_cmd $2${NC}\n"
    
    eval "$pytest_cmd $2"
}

# Test suite functions
run_unit_tests() {
    run_test_suite "unit" "quantum_crypto/completion/testing/test_unit.py quantum_crypto/completion/testing/test_quantum_*.py"
}

run_integration_tests() {
    run_test_suite "integration" "quantum_crypto/completion/testing/test_network*.py quantum_crypto/completion/testing/integration_tests.py"
}

run_system_tests() {
    run_test_suite "system" "quantum_crypto/completion/testing/system_tests.py"
}

run_all_tests() {
    run_test_suite "all" "quantum_crypto/completion/testing/"
    run_symbolic_tests
}

run_symbolic_tests() {
    run_test_suite "symbolic" "trading-platform/symbolic_trading/tests/symbolic/"
}

# Main menu
while true; do
    print_header
    
    echo -e "${YELLOW}Configuration:${NC}"
    echo "├── Environment: $TEST_ENV"
    echo "├── Verbose: $VERBOSE"
    echo "├── Coverage: $COVERAGE"
    echo "├── Fail Fast: $FAIL_FAST"
    echo "└── Max Failures: $MAX_FAIL"
    echo
    
    echo "Please select test suite to run:"
    echo "1) Run Unit Tests"
    echo "2) Run Integration Tests"
    echo "3) Run System Tests"
    echo "4) Run Symbolic Math Tests"
    echo "5) Run All Tests" 
    echo "6) Show Help"
    echo "7) Exit"
    
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            run_unit_tests
            ;;
        2)
            run_integration_tests
            ;;
        3)
            run_system_tests
            ;;
        4)
            run_symbolic_tests
            ;;
        5)
            run_all_tests
            ;;
        6)
            print_help
            ;;
        7)
            echo -e "\n${BLUE}Exiting test runner...${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}Invalid choice. Please select 1-7.${NC}\n"
            sleep 1
            clear
            ;;
    esac
    
    echo -e "\nPress Enter to return to menu..."
    read
    clear
done
