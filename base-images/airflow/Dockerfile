FROM apache/airflow:3.1.3-python3.13

COPY --chown=airflow:0 apache_airflow_providers_opensearch-1.7.5-py3-none-any.whl /tmp/

RUN pip install --no-cache-dir \
    apache-airflow-providers-fab==3.0.2 \
    "connexion[flask]<3.0" \
    flask-appbuilder==5.0.1 \
    flask-session \
    opensearch-py \
    /tmp/apache_airflow_providers_opensearch-1.7.5-py3-none-any.whl

RUN rm /tmp/apache_airflow_providers_opensearch-1.7.5-py3-none-any.whl



