from pydantic import BaseModel
import dataclasses
import pathlib
from typing import List, Tuple, Optional


class BaseQueryBuilderSettings(BaseModel):
    # источник: PG или Kafka
    source_type: str
    # название структуры из источника: топик или таблица
    source_name: str
    # указание на типы событий, None - все
    fields: List[str] = []


class SqlQueryBuilderSettings(BaseQueryBuilderSettings):
    """Специализированный класс настроек, для SQL."""
    dbschema: str = 'content'
    where_conditions: List[str] = []
    limit: int = 100
    offset: int = 0
