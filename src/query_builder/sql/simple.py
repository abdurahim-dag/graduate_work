from core import SqlQueryBuilderSettings
from query_builder import QueryBuilderBase


class SimpleSQLQueryBuilder(QueryBuilderBase):
    """Простой генератор запросов."""
    def __init__(self, settings: SqlQueryBuilderSettings):
        """
        Инициализирует объект построителя SQL-запросов.

        Пример:
            sql_builder = SQLQueryBuilder(settings)
        """
        self._settings = settings

    def _build_where_conditions(self) -> str:
        return "WHERE " + " AND ".join(self._settings.where_conditions)\
            if self._settings.where_conditions else ""

    def _build_limit_offset(self) -> str:
        limit = f"LIMIT {self._settings.limit}" if self._settings.limit else ""
        offset = f"OFFSET {self._settings.offset}" if self._settings.offset else ""
        return f"{limit} {offset}"

    def build_query(self) -> str:
        """
        Строит SQL-запрос на основе настроек ETL.

        Пример:
            sql_query = sql_builder.build_query()
        """
        fields = ", ".join(self._settings.fields)\
            if self._settings.fields else "*"
        select_clause = f"SELECT {fields}"

        from_clause = f"FROM {self._settings.schema}.{self._settings.source_name}"

        query = f"""{select_clause} {from_clause}
            {self._build_where_conditions()}"""

        limit_offset = self._build_limit_offset()
        if limit_offset:
            query += f" {limit_offset}"

        return query.replace('\n', '').strip()
