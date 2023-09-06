from typing import Any
import dataclasses
import pathlib


@dataclasses.dataclass
class PostgresODSLoaderSettings:
    host: str
    port: int
    username: str
    password: str
    dbname: str
    batch_size: int

    dir_path: pathlib.PurePath
    src_prefix_file: str

    dbschema: str = 'ods'

    @property
    def conn_params(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"

@dataclasses.dataclass
class ESLoaderSettings:
    # Settings for ElasticsearchLoader.
    es_host: str
    es_port: str

    dir_path: pathlib.PurePath
    index_name: str
    src_prefix_file: str
    model: Any = None

    @property
    def conn_params(self):
        return f"http://{self.es_host}:{self.es_port}"

