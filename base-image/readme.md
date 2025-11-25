## Build and push image for Linux and Mac
1. Make sure the patched `apache_airflow_providers_opensearch` wheel is in the same directory as the `Dockerfile`.
2. Make sure you are logged in to the CERN registry.
3. Run the following command:
    ```bash
    docker buildx build --no-cache \
    --platform linux/amd64,linux/arm64 \
    -t registry.cern.ch/cern-sis/scoap3/airflow-base:3.1.3 \
    --push \
    .
    ```

4. Enjoy!
