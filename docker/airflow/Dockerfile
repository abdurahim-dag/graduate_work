FROM apache/airflow:latest
ARG BUILD_ENVIRONMENT=dev

# Compulsory to switch parameter
ENV PIP_USER=false

#python venv setup
RUN python3 -m venv /opt/airflow/venv

# Install dependencies:
COPY ./requirements .

RUN /opt/airflow/venv/bin/pip install --no-cache-dir -r ${BUILD_ENVIRONMENT}.txt
ENV PIP_USER=true
