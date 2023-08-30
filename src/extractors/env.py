from pydantic import BaseConfig, Field

class Settings(BaseConfig):

    kafka_host: str = Field("localhost", env="KAFKA_HOST")
    kafka_port: str = Field("9092", env="KAFKA_PORT")

    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    group_id: str = Field("group_watching_movies", env="KAFKA_GROUP_ID")
    topic: str = Field("watching_movies", env="KAFKA_TOPIC")
    batch_timeout: int = Field(10, env="BATCH_TIMEOUT")  # in sec
    batch_size: int = Field(10, env="BATCH_SIZE")

    ch_host: str = Field("localhost", env="CLICKHOUSE_HOST")
    ch_port: int = Field(18123, env="CLICKHOUSE_PORT")
    ch_db: str = Field("movix_db", env="CLICKHOUSE_DATABASE")
    ch_table: str = Field("watching_movies", env="CLICKHOUSE_TABLE")
    ch_username: str = Field("movix", env="CLICKHOUSE_USERNAME")
    ch_password: str = Field("qwe123", env="CLICKHOUSE_PASSWORD")

    staging_host: str = Field("localhost", env="STAGING_HOST")
    staging_port: int = Field(5432, env="STAGING_PORT")
    staging_username: str = Field("etl", env="STAGING_USERNAME")
    staging_password: str = Field("123qwe", env="STAGING_PASSWORD")
    staging_dbname: str = Field("etl", env="STAGING_DBNAME")


    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"

