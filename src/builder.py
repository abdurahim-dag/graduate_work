from typing import List, Tuple, Optional


class ETLSettings:
    def __init__(self):
        """Инициализирует объект настроек ETL."""
        self.table_name: Optional[str] = None
        self.fields: List[str] = []
        self.aggregations: List[Tuple[str, str]] = []
        self.group_by: List[str] = []
        self.where_conditions: List[str] = []
        self.order_by: List[Tuple[str, str]] = []
        self.subquery: Optional[str] = None

    def set_table_name(self, table_name: str) -> None:
        """
        Устанавливает имя таблицы для запроса.

        Пример:
            etl_settings.set_table_name("users")
        """
        self.table_name = table_name

    def add_field(self, field: str) -> None:
        """
        Добавляет поле для выборки в запросе.

        Пример:
            etl_settings.add_field("username")
        """
        self.fields.append(field)

    def add_aggregation(self, field: str, function: str) -> None:
        """
        Добавляет функцию агрегации для поля.

        Пример:
            etl_settings.add_aggregation("price", "SUM")
        """
        self.aggregations.append((function, field))

    def add_group_by(self, field: str) -> None:
        """
        Добавляет поле для группировки в запросе.

        Пример:
            etl_settings.add_group_by("product_id")
        """
        self.group_by.append(field)

    def add_where_condition(self, condition: str) -> None:
        """
        Добавляет условие фильтрации для запроса.

        Пример:
            etl_settings.add_where_condition("price > 100")
        """
        self.where_conditions.append(condition)

    def add_order_by(self, field: str, direction: str = "ASC") -> None:
        """
        Добавляет поле и направление сортировки для запроса.

        Пример:
            etl_settings.add_order_by("created_at", "DESC")
        """
        self.order_by.append((field, direction))

    def set_subquery(self, subquery: str) -> None:
        """
        Устанавливает подзапрос для поля FROM.

        Пример:
            etl_settings.set_subquery(
                "SELECT * FROM sales_archive WHERE year = 2022"
            )
        """
        self.subquery = subquery

    def __str__(self) -> str:
        return f"""
            ETLSettings:
                table_name={self.table_name},
                fields={self.fields},
                aggregations={self.aggregations},
                group_by={self.group_by},
                where_conditions={self.where_conditions},
                order_by={self.order_by},
                subquery={self.subquery}"""


class SQLQueryBuilder:
    def __init__(self, etl_settings: ETLSettings):
        """
        Инициализирует объект построителя SQL-запросов.

        Пример:
            sql_builder = SQLQueryBuilder(etl_settings)
        """
        self.etl_settings = etl_settings

    def _build_aggregations(self) -> str:
        aggregation_strings = [
            f"{function.upper()}({field}) AS {function}_{field}"
            for function, field in self.etl_settings.aggregations
        ]
        return ", ".join(aggregation_strings)

    def _build_group_by(self) -> str:
        return "GROUP BY " + ", ".join(self.etl_settings.group_by)\
            if self.etl_settings.group_by else ""

    def _build_where_conditions(self) -> str:
        return "WHERE " + " AND ".join(self.etl_settings.where_conditions)\
            if self.etl_settings.where_conditions else ""

    def _build_order_by(self) -> str:
        order_strings = [
            f"{field} {direction}" for field, direction
            in self.etl_settings.order_by
        ]
        return "ORDER BY " + ", ".join(order_strings) if order_strings else ""

    def build_query(self) -> str:
        """
        Строит SQL-запрос на основе настроек ETL.

        Пример:
            sql_query = sql_builder.build_query()
        """
        fields = ", ".join(self.etl_settings.fields)\
            if self.etl_settings.fields else "*"
        from_clause = f"FROM ({self.etl_settings.subquery}) AS subquery_table"\
            if self.etl_settings.subquery\
            else f"FROM {self.etl_settings.table_name}"
        select_clause = f"SELECT {self._build_aggregations()}"\
            if self.etl_settings.aggregations else f"SELECT {fields}"
        query = f"""{select_clause} {from_clause}
        {self._build_where_conditions()}
        {self._build_group_by()} {self._build_order_by()}"""
        return query.replace('\n', '').strip()


if __name__ == '__main__':
    # Создаем объект настроек ETL
    etl_settings = ETLSettings()

    # Устанавливаем имя таблицы
    etl_settings.set_table_name("products")

    # Добавляем поля для выборки
    etl_settings.add_field("product_id")
    etl_settings.add_field("product_name")

    # Добавляем функции агрегации
    etl_settings.add_aggregation("price", "AVG")
    etl_settings.add_aggregation("quantity", "SUM")

    # Добавляем условие группировки
    etl_settings.add_group_by("product_category")

    # Добавляем условия фильтрации
    etl_settings.add_where_condition("price > 50")
    etl_settings.add_where_condition("quantity > 10")

    # Добавляем сортировку
    etl_settings.add_order_by("product_name", "ASC")

    # Устанавливаем подзапрос для поля FROM
    etl_settings.set_subquery(
        "SELECT * FROM products_archive WHERE year = 2022"
    )

    # Создаем объект построителя SQL-запросов и передаем ему настройки ETL
    sql_builder = SQLQueryBuilder(etl_settings)

    # Строим SQL-запрос
    sql_query = sql_builder.build_query()

    # Выводим полученный SQL-запрос
    print(sql_query)
