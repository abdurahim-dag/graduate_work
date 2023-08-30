from pydantic import BaseModel
import dataclasses
import pathlib
from typing import List, Tuple, Optional


class BaseExtractorSettings(BaseModel):
    # источник: PG или Kafka
    source_type: str
    # название структуры из источника: топик или таблица
    source_name: str
    # указание на типы событий, None - все
    fields: List[str] = []


class SqlExtractorSettings(BaseExtractorSettings):
    """Специализированный класс настроек, для SQL."""
    schema: str = 'staging'
    where_conditions: List[str] = []


class PostgresExtractorSettings(SqlExtractorSettings):
    host: str
    port: int
    username: str
    password: str
    dbname: str
    batch_size: int

    @property
    def conn_params(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"


@dataclasses.dataclass
class TransformSettings:
    file_name: str
    file_path: pathlib.Path
    index_name: str
    schema: str = 'staging'


