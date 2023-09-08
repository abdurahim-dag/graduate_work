import dataclasses
import pathlib
from typing import Any


@dataclasses.dataclass
class BaseLoaderSettings:
    host: str
    port: int
    dir_path: pathlib.PurePath
    src_prefix_file: str
    model: Any


@dataclasses.dataclass
class ODSLoaderSettings(BaseLoaderSettings):
    username: str
    password: str
    dbname: str
    batch_size: int
    schema: str = 'ods'

    @property
    def conn_str(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"


@dataclasses.dataclass
class ESLoaderSettings(BaseLoaderSettings):
    index_name: str

    @property
    def conn_str(self) -> str:
        return f"http://{self.host}:{self.port}"
