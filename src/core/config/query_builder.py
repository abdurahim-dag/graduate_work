from typing import List
from typing import Tuple

from pydantic import BaseModel


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
    order_by: List[Tuple[str, str]] = [('modified', 'ASC')]
    limit: int = 100
    offset: int = 0
