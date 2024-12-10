#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored header
print_header() {
    echo -e "${BLUE}================================================"
    echo -e "    Quantum Cryptocurrency Installation Script"
    echo -e "================================================${NC}\n"
}

# Function to check dependencies
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install Python 3.9 or later.${NC}"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}pip3 is not installed. Please install pip3.${NC}"
        exit 1
    fi
    
    # Check Docker if needed
    if [ "$1" == "docker" ] && ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
        exit 1
    fi
    
    if [ "$1" == "docker" ] && ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}All required dependencies are installed.${NC}\n"
}

# Function to install local deployment
install_local() {
    echo -e "${BLUE}Installing local deployment...${NC}"
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install requirements
    pip install -r quantum_crypto/requirements.txt
    
    # Make start script executable
    chmod +x start.sh
    
    echo -e "${GREEN}Local installation completed!${NC}"
    echo -e "To start the node, run: ${BLUE}./start.sh${NC}\n"
}

# Function to install Docker deployment
install_docker() {
    echo -e "${BLUE}Installing Docker deployment...${NC}"
    
    # Build and start the containers
    docker-compose up --build -d
    
    echo -e "${GREEN}Docker installation completed!${NC}"
    echo -e "To view the cluster status, run: ${BLUE}docker-compose ps${NC}"
    echo -e "To view logs, run: ${BLUE}docker-compose logs -f${NC}"
    echo -e "To stop the cluster, run: ${BLUE}docker-compose down${NC}\n"
}

# Main menu
main_menu() {
    while true; do
        print_header
        
        echo "Please select installation type:"
        echo "1) Local Installation (Single Node)"
        echo "2) Docker Installation (Multi-Node Cluster)"
        echo "3) Exit"
        
        read -p "Enter your choice (1-3): " choice
        
        case $choice in
            1)
                check_dependencies "local"
                install_local
                break
                ;;
            2)
                check_dependencies "docker"
                install_docker
                break
                ;;
            3)
                echo -e "\n${BLUE}Exiting installation script...${NC}"
                exit 0
                ;;
            *)
                echo -e "\n${RED}Invalid choice. Please select 1-3.${NC}\n"
                sleep 1
                clear
                ;;
        esac
    done
}

# Start the script
main_menu
