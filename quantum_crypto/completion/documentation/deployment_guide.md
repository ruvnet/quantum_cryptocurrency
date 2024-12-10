# Deployment Guide

## Prerequisites
- **Docker**: Ensure Docker is installed on the deployment machine.
- **Access to Willow Quantum Chip**: Required for quantum operations (simulation is possible for testing).

## Deployment Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/quantum-currency-project.git
    cd quantum-currency-project
    ```

2. **Set Up Environment Variables**
    - Copy the sample environment file:
        ```bash
        cp config/sample.env config/.env
        ```
    - Edit `config/.env` with necessary configurations.

3. **Build Docker Images**
    ```bash
    cd completion/deployment/docker
    docker-compose build
    ```

4. **Start the Containers**
    ```bash
    docker-compose up -d
    ```

5. **Verify Deployment**
    - Check the logs to ensure all services are running correctly:
        ```bash
        docker-compose logs -f
        ```

## Rollback Strategy
If deployment issues arise, perform the following steps to rollback:

1. **Stop Current Containers**
    ```bash
    docker-compose down
    ```

2. **Revert to Previous Image**
    - If using tagged releases, pull the previous stable image:
        ```bash
        docker-compose pull your_service:previous_tag
        ```

3. **Restart Containers with Previous Image**
    ```bash
    docker-compose up -d
    ```
