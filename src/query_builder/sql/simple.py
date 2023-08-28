from core import SqlEventSubscription
from .base import QueryBuilderBase


class SimpleSQLQueryBuilder(QueryBuilderBase):
    """Простой генератор запросов."""
    def __init__(self, settings: SqlEventSubscription):
        """
        Инициализирует объект построителя SQL-запросов.

        Пример:
            sql_builder = SQLQueryBuilder(etl_settings)
        """
        self._settings = settings

    def _build_aggregations(self) -> str:
        aggregation_strings = [
            f"{function.upper()}({field}) AS {function}_{field}"
            for function, field in self._settings.aggregations
        ]
        return ", ".join(aggregation_strings)

    def _build_group_by(self) -> str:
        return "GROUP BY " + ", ".join(self._settings.group_by)\
            if self._settings.group_by else ""

    def _build_where_conditions(self) -> str:
        return "WHERE " + " AND ".join(self._settings.where_conditions)\
            if self._settings.where_conditions else ""

    def _build_order_by(self) -> str:
        order_strings = [
            f"{field} {direction}" for field, direction
            in self._settings.order_by
        ]
        return "ORDER BY " + ", ".join(order_strings) if order_strings else ""

    def build_query(self) -> str:
        """
        Строит SQL-запрос на основе настроек ETL.

        Пример:
            sql_query = sql_builder.build_query()
        """
        fields = ", ".join(self._settings.fields)\
            if self._settings.fields else "*"

        from_clause = f"FROM {self._settings.schema}.{self._settings.source_name}"

        select_clause = f"SELECT {self._build_aggregations()}"\
            if self._settings.aggregations else f"SELECT {fields}"
        query = f"""{select_clause} {from_clause}
        {self._build_where_conditions()}
        {self._build_group_by()} {self._build_order_by()}"""
        return query.replace('\n', '').strip()
