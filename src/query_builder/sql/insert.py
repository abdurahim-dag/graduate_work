class InsertSQLBuilder:
    def __init__(self, schema_name, table_name, insert_data, conflict_columns=None, update_data=None):
        """
        Инициализация объекта построителя запросов на вставку с ON CONFLICT.

        :param table_name: Имя таблицы, в которую вы хотите вставить данные.
        :param insert_data: Словарь с данными для вставки в формате {column_name: value}.
        :param conflict_columns: Список колонок, на которых будет проверяться конфликт (ON CONFLICT).
        :param update_data: Словарь с данными для обновления (если конфликт разрешается).
        """
        self.schema_name = schema_name
        self.table_name = table_name
        self.insert_data = insert_data
        self.conflict_columns = conflict_columns
        self.update_data = update_data

    def build_query(self):
        # Создание части запроса для вставки данных
        insert_query = f"INSERT INTO {self.schema_name}.{self.table_name} ("
        columns = ", ".join(self.insert_data.keys())
        values = ", ".join([f"'{value}'" for value in self.insert_data.values()])
        insert_query += f"{columns}) VALUES ({values})"

        # Добавление ON CONFLICT
        if self.conflict_columns:
            conflict_columns = ", ".join(self.conflict_columns)
            insert_query += f" ON CONFLICT ({conflict_columns})"

            # Добавление обновления данных при конфликте (если указано)
            if self.update_data:
                update_values = ", ".join([f"{column} = '{self.insert_data[column]}'" for column in self.update_data])
                insert_query += f" DO UPDATE SET {update_values}"

        return insert_query

