#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored header
print_header() {
    echo -e "${BLUE}================================================"
    echo -e "    Quantum Cryptocurrency Test Runner"
    echo -e "================================================${NC}\n"
}

# Function to run unit tests
run_unit_tests() {
    echo -e "${BLUE}Running unit tests...${NC}"
    cd quantum_crypto && PYTHONPATH=/workspaces/quantum_cryptocurrency python -m pytest completion/testing/test_unit.py -v
}

# Function to run integration tests
run_integration_tests() {
    echo -e "${BLUE}Running integration tests...${NC}"
    cd quantum_crypto && PYTHONPATH=/workspaces/quantum_cryptocurrency python -m pytest completion/testing/integration_tests.py -v
}

# Function to run system tests
run_system_tests() {
    echo -e "${BLUE}Running system tests...${NC}"
    cd quantum_crypto && PYTHONPATH=/workspaces/quantum_cryptocurrency python -m pytest completion/testing/system_tests.py -v
}

# Function to run all tests
run_all_tests() {
    echo -e "${BLUE}Running all tests...${NC}"
    cd quantum_crypto && PYTHONPATH=/workspaces/quantum_cryptocurrency python -m pytest completion/testing/ -v
}

# Main menu
while true; do
    print_header
    
    echo "Please select test suite to run:"
    echo "1) Run Unit Tests"
    echo "2) Run Integration Tests"
    echo "3) Run System Tests"
    echo "4) Run All Tests"
    echo "5) Exit"
    
    read -p "Enter your choice (1-5): " choice
    
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
            run_all_tests
            ;;
        5)
            echo -e "\n${BLUE}Exiting test runner...${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}Invalid choice. Please select 1-5.${NC}\n"
            sleep 1
            clear
            ;;
    esac
    
    echo -e "\nPress Enter to return to menu..."
    read
    clear
done
