import pathlib

from pydantic import BaseModel


class PostgresExtractorSettings(BaseModel):
    host: str
    port: int
    username: str
    password: str
    dbname: str
    batch_size: int
    dir_path: pathlib.PurePath
    filename_prefix: str = 'extract'
    date_field_name: str = 'modified'

    @property
    def conn_params(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
