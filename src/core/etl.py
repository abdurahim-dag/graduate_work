from pydantic import BaseModel


class EventSubscription(BaseModel):
    # источник: PG или Kafka
    source_type: str
    # название структуры из источника: топик или таблица
    source_name: str
    # указание на типы событий, None - все
    event_type: str | None = None
    fields: list[str]
