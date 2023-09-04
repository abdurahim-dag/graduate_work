from pydantic_settings import BaseSettings
from pydantic import Field
import pathlib

class Settings(BaseSettings):

    kafka_host: str = Field(default="localhost", env="KAFKA_HOST")
    kafka_port: str = Field(default="9092", env="KAFKA_PORT")

    state_host: str = Field(default="localhost", env="STATE_HOST")
    state_port: int = Field(default=6379, env="STATE_PORT")

    group_id: str = Field(default="group_watching_movies", env="KAFKA_GROUP_ID")
    topic: str = Field(default="watching_movies", env="KAFKA_TOPIC")
    batch_timeout: int = Field(default=10, env="BATCH_TIMEOUT")  # in sec
    batch_size: int = Field(default=100, env="BATCH_SIZE")

    ch_host: str = Field(default="localhost", env="CLICKHOUSE_HOST")
    ch_port: int = Field(default=18123, env="CLICKHOUSE_PORT")
    ch_db: str = Field(default="movix_db", env="CLICKHOUSE_DATABASE")
    ch_table: str = Field(default="watching_movies", env="CLICKHOUSE_TABLE")
    ch_username: str = Field(default="movix", env="CLICKHOUSE_USERNAME")
    ch_password: str = Field(default="qwe123", env="CLICKHOUSE_PASSWORD")

    staging_host: str = Field(default="localhost", env="STAGING_HOST")
    staging_port: int = Field(default=5433, env="STAGING_PORT")
    staging_username: str = Field(default="etl", env="STAGING_USERNAME")
    staging_password: str = Field(default="123qwe", env="STAGING_PASSWORD")
    staging_dbname: str = Field(default="etl", env="STAGING_DBNAME")

    movies_host: str = Field(default="localhost", env="MOVIES_HOST")
    movies_port: int = Field(default=5432, env="MOVIES_PORT")
    movies_username: str = Field(default="app", env="MOVIES_USERNAME")
    movies_password: str = Field(default="qwe123", env="MOVIES_PASSWORD")
    movies_dbname: str = Field(default="movies_database", env="MOVIES_DBNAME")

    extract_dir_path: pathlib.PurePath = pathlib.PurePath('./data')

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"

