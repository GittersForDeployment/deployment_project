FROM apache/airflow:2.8.1-python3.11

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
           curl \
           gnupg2 \
           default-mysql-client \
           netcat-traditional \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY dags/ /opt/airflow/dags/
COPY entrypoint.sh /entrypoint.sh

USER root
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

USER airflow

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]