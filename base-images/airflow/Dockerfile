FROM apache/airflow:3.1.3-python3.13
COPY plugins/ /opt/airflow/plugins/
RUN pip install --no-cache-dir \
    apache-airflow-providers-fab==3.0.2 \
    "connexion[flask]<3.0" \
    flask-appbuilder==5.0.1 \
    flask-session
