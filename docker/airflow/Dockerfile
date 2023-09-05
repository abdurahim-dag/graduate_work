FROM apache/airflow:2.7.0-python3.10
ARG BUILD_ENVIRONMENT=dev

USER root
RUN mkdir /data \
  && chown airflow: /data
USER airflow

# Compulsory to switch parameter
ENV PIP_USER=false

#python venv setup
RUN python3 -m venv /opt/airflow/venv

# Install dependencies:
COPY ./requirements .

RUN /opt/airflow/venv/bin/pip install --no-cache-dir -r ${BUILD_ENVIRONMENT}.txt
ENV PIP_USER=true
