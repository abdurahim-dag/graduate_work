import os

from pydantic import BaseSettings, Field


class ModelConfig:
    allow_population_by_field_name = True


class Settings(BaseSettings):

    project_name: str = "etl-on-steroids"

    kafka_host: str = Field("localhost", env="KAFKA_HOST")
    kafka_port: str = Field("9092", env="KAFKA_PORT")

    airflow_host: str = Field("localhost", env="AIRFLOW_HOST")
    airflow_port: int = Field(6379, env="AIRFLOW_PORT")
    airflow_username: str = Field("airflow", env="AIRFLOW_USERNAME")
    airflow_password: str = Field("password", env="AIRFLOW_PASSWORD")
    airflow_conn_pg: str = Field("postgresql", env="AIRFLOW_PGCONNAME")

    group_id: str = Field("group_watching_movies", env="KAFKA_GROUP_ID")
    topic: str = Field("watching_movies", env="KAFKA_TOPIC")
    batch_timeout: int = Field(10, env="BATCH_TIMEOUT")  # in sec
    batch_size: int = Field(10, env="BATCH_SIZE")

    pg_host: str = Field("postgres", env="POSTGRES_HOST")
    pg_port: int = Field(5432, env="POSTGRES_PORT")
    pg_username: str = Field("etl", env="POSTGRES_USERNAME")
    pg_password: str = Field("123qwe", env="POSTGRES_PASSWORD")
    pg_db: str = Field("staging", env="POSTGRES_DB")

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"

    @property
    def airflow_connection_pg_endpoint(self):
        return f"http://{self.airflow_port}:{self.airflow_port}/api/v1/connections/{self.airflow_conn_pg}"

    base_dir = os.path.dirname(os.path.dirname(__file__))


settings = Settings()
