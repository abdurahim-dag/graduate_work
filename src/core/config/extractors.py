from pydantic import BaseModel
import dataclasses
import pathlib
from typing import List, Tuple, Optional


class PostgresExtractorSettings(BaseModel):
    host: str
    port: int
    username: str
    password: str
    dbname: str
    batch_size: int
    filename_prefix: str = 'extract'

    @property
    def conn_params(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
