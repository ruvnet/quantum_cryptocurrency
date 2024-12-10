# Rollback Strategy

In case of deployment failure or critical issues post-deployment, follow these steps to rollback to a stable state.

## Steps

1. **Stop Current Deployment**
    ```bash
    docker-compose down
    ```

2. **Revert to Previous Stable Image**
    - Pull the previous stable Docker image from the registry:
        ```bash
        docker pull yourusername/quantum_currency_app:stable
        ```

3. **Update docker-compose.yml**
    - Modify the `docker-compose.yml` to use the stable image tag:
        ```yaml
        services:
          quantum_currency:
            image: yourusername/quantum_currency_app:stable
            ...
        ```

4. **Restart Services with Stable Image**
    ```bash
    docker-compose up -d
    ```

5. **Verify Rollback**
    - Check the logs to ensure the application is running the stable version:
        ```bash
        docker-compose logs -f
        ```

## Prevention
- **Version Tagging**: Always tag Docker images with version numbers.
- **Testing**: Ensure thorough testing before deploying new changes.
- **Backup**: Regularly backup configuration files and data.
