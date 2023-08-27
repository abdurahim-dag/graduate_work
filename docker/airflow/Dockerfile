FROM apache/airflow:2.7.0
ARG BUILD_ENVIRONMENT=dev

COPY ./requirements .
RUN pip install --no-cache-dir -r ${BUILD_ENVIRONMENT}.txt
