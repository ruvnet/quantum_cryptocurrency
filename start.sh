#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored header
print_header() {
    echo -e "${BLUE}================================================"
    echo -e "    Quantum Cryptocurrency Node Launcher"
    echo -e "================================================${NC}\n"
}

# Function to start local node
start_local() {
    echo -e "${BLUE}Starting local node...${NC}"
    cd /workspaces/quantum_cryptocurrency
    PYTHONPATH=$PYTHONPATH:/workspaces/quantum_cryptocurrency python quantum_crypto/src/main.py
}

# Function to manage Docker cluster
start_docker() {
    echo -e "${BLUE}Starting Docker cluster...${NC}"
    
    # Check if .env exists, if not copy sample
    if [ ! -f "quantum_crypto/config/.env" ]; then
        echo -e "${YELLOW}Creating .env file from sample...${NC}"
        cp quantum_crypto/config/sample.env quantum_crypto/config/.env
    fi
    
    while true; do
        echo -e "\n${YELLOW}Docker Cluster Management:${NC}"
        echo "1) Start Cluster"
        echo "2) Stop Cluster"
        echo "3) View Logs"
        echo "4) List Containers"
        echo "5) Restart Cluster"
        echo "6) Check Container Health"
        echo "7) Return to Main Menu"
        
        read -p "Enter your choice (1-7): " docker_choice
        
        case $docker_choice in
            1)
                cd /workspaces/quantum_cryptocurrency
                docker-compose -f quantum_crypto/completion/deployment/docker/docker-compose.yml up -d
                echo -e "${GREEN}Docker cluster started!${NC}"
                ;;
            2)
                docker-compose -f quantum_crypto/completion/deployment/docker/docker-compose.yml down
                echo -e "${YELLOW}Docker cluster stopped.${NC}"
                ;;
            3)
                docker-compose -f quantum_crypto/completion/deployment/docker/docker-compose.yml logs -f
                ;;
            4)
                echo -e "\n${BLUE}Active Containers:${NC}"
                docker-compose -f quantum_crypto/completion/deployment/docker/docker-compose.yml ps
                ;;
            5)
                docker-compose -f quantum_crypto/completion/deployment/docker/docker-compose.yml restart
                echo -e "${GREEN}Docker cluster restarted!${NC}"
                ;;
            6)
                echo -e "\n${BLUE}Container Health Status:${NC}"
                docker ps --format "table {{.Names}}\t{{.Status}}"
                ;;
            7)
                return
                ;;
            *)
                echo -e "\n${RED}Invalid choice. Please select 1-7.${NC}"
                ;;
        esac
        
        echo -e "\nPress Enter to continue..."
        read
    done
}

# Main menu
while true; do
    print_header
    
    echo "Please select deployment type:"
    echo "1) Start Local Node"
    echo "2) Start Docker Cluster"
    echo "3) Exit"
    
    read -p "Enter your choice (1-3): " choice
    
    case $choice in
        1)
            start_local
            break
            ;;
        2)
            start_docker
            break
            ;;
        3)
            echo -e "\n${BLUE}Exiting launcher...${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}Invalid choice. Please select 1-3.${NC}\n"
            sleep 1
            clear
            ;;
    esac
done
