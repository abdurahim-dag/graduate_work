import dataclasses
import pathlib


@dataclasses.dataclass
class BaseExtractorSettings:
    batch_size: int = 100
    dir_path: pathlib.PurePath = pathlib.PurePath('.\\')
    filename_prefix: str = 'extract'
    date_field_name: str = 'modified'


@dataclasses.dataclass
class PostgresExtractorSettings(BaseExtractorSettings):
    host: str = 'localhost'
    port: int = 5432
    username: str = 'app'
    password: str = '123qwe'
    dbname: str = 'etl'
    schema: str = 'content'

    @property
    def conn_params(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
