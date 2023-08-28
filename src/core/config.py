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


class PostgresExtractorSettings(BaseExtractorSettings):
    """Специализированный класс настроек, для SQL."""
    schema: str = 'staging'
    aggregations: List[Tuple[str, str]] = []
    group_by: List[str] = []
    where_conditions: List[str] = []
    order_by: List[Tuple[str, str]] = []


@dataclasses.dataclass
class TransformSettings:
    file_name: str
    file_path: pathlib.Path
    index_name: str
    schema: str = 'staging'


@dataclasses.dataclass
class SourcePostgresSettings:
    host: str
    port: int
    username: str
    password: str
