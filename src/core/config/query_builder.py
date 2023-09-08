import dataclasses
from typing import List, Tuple


@dataclasses.dataclass
class BaseQueryBuilderSettings:
    # источник: PG или Kafka
    source_type: str
    # название структуры из источника: топик или таблица
    source_name: str
    # указание на поля, None - все
    fields: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SqlQueryBuilderSettings(BaseQueryBuilderSettings):
    """Специализированный класс настроек, для SQL."""

    schema: str = 'content'
    where_conditions: list[str] = dataclasses.field(default_factory=list)
    order_by: list[tuple[str, str]] = dataclasses.field(
        default_factory=list[('modified', 'ASC')]
    )
    limit: int = 100
    offset: int = 0
