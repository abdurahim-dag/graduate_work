from core import SqlExtractorSettings
from query_builder import QueryBuilderBase


class SimpleSQLQueryBuilder(QueryBuilderBase):
    """Простой генератор запросов."""
    def __init__(self, settings: SqlExtractorSettings):
        """
        Инициализирует объект построителя SQL-запросов.

        Пример:
            sql_builder = SQLQueryBuilder(etl_settings)
        """
        self._settings = settings

    def _build_where_conditions(self) -> str:
        return "WHERE " + " AND ".join(self._settings.where_conditions)\
            if self._settings.where_conditions else ""

    def build_query(self) -> str:
        """
        Строит SQL-запрос на основе настроек ETL.

        Пример:
            sql_query = sql_builder.build_query()
        """
        fields = ", ".join(self._settings.fields)\
            if self._settings.fields else "*"
        from_clause = f"FROM {self._settings.schema}.{self._settings.source_name}"
        select_clause = f"SELECT {fields}"\
            if self._settings.aggregations else f"SELECT {fields}"

        query = f"""{select_clause} {from_clause}
            {self._build_where_conditions()}"""

        return query.replace('\n', '').strip()
