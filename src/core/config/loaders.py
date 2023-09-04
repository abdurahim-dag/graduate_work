from pydantic import BaseModel
import dataclasses
import pathlib
from typing import List, Tuple, Optional


@dataclasses.dataclass
class PostgresStagingLoaderSettings:
    host: str
    port: int
    username: str
    password: str
    dbname: str
    batch_size: int

    dir_path: pathlib.PurePath
    src_prefix_file: str

    dbschema: str = 'staging'

    @property
    def conn_params(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"


