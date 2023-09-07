from typing import List
from typing import Tuple

import dataclasses


@dataclasses.dataclass
class BaseQueryBuilderSettings:
    # источник: PG или Kafka
    source_type: str
    # название структуры из источника: топик или таблица
    source_name: str
    # указание на поля, None - все
    fields: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SqlQueryBuilderSettings(BaseQueryBuilderSettings):
    """Специализированный класс настроек, для SQL."""
    dbschema: str = 'content'
    where_conditions: List[str] = dataclasses.field(default_factory=list)
    order_by: List[Tuple[str, str]] = dataclasses.field(default_factory = list[('modified', 'ASC'),])
    limit: int = 100
    offset: int = 0
