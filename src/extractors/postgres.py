import json
from psycopg.rows import dict_row
from pathlib import PurePath, Path

import pendulum
import psycopg

from utils import on_exception
from utils import logger
from utils import MyEncoder
from core import PostgresExtractorSettings, SqlQueryBuilderSettings

from states import BaseStorageState
from query_builder import QueryBuilderBase
from typing import Type
from models import EtlState

class PostgresExtractor:
    """Extract batches rows to files."""
    def __init__(
            self,
            settings: PostgresExtractorSettings,
            storage_state: BaseStorageState,
            query_builder_type: Type[QueryBuilderBase],
            query_builder_settings: SqlQueryBuilderSettings,

    ) -> None:
        self._settings = settings
        self._storage_state = storage_state
        self._query_builder_type = query_builder_type
        self._query_builder_settings = query_builder_settings


    def _get_filname(self, prefix: str, name: str, date: str, offset: str) -> str:
        return f"{prefix}-{name}-{date}-{offset}.json"

    def _get_filepath(self, date: str, offset: str) -> str:
        file_name = self._get_filname(
            prefix=self._settings.filename_prefix,
            name=self._query_builder_settings.source_name,
            date=date,
            offset=offset
        )
        return str(self._settings.dir_path / file_name)


    @on_exception(
        exception=psycopg.DatabaseError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def _extract(self):
        """Extract rows to files."""
        with psycopg.connect(conninfo=self._settings.conn_params, row_factory=dict_row) as conn:
            with conn.cursor() as curs:

                while True:
                    self._query_builder_settings.offset = self._state.offset

                    sql = self._query_builder_type(settings=self._query_builder_settings).build_query()

                    curs.execute(sql)

                    rows = curs.fetchall()
                    if len(rows) == 0:
                        break

                    file_path = self._get_filepath(
                        date=str(self._state.date_from.date()),
                        offset=str(self._state.offset)
                    )

                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(rows, f, cls=MyEncoder, sort_keys=True, ensure_ascii=False)

                    # Сохраняем каждый выполненный шаг.
                    self._state.offset += self._query_builder_settings.limit
                    self._storage_state.save(self._state)
                    logger.info("Extracted file %s", file_path)

                # Сохраним offset = 0, сигнализирующем о новом запуске.
                # Установим дату началу следующего запуска.
                self._state.date_from = self._state.date_to
                self._state.offset = 0
                self._storage_state.save(self._state)

    def run(self):
        """Функция предварительной подготовки и запуска основной задачи экспорта."""
        self._state: EtlState = self._storage_state.retrieve()
        # В первый раз создаём стартовые параметры состояния
        if self._state is None:
            self._state = EtlState()
        # Если это новый запуск, то установим конечную дату 'до сейчас'
        if self._state.offset == 0:
            self._state.date_to = pendulum.now()

        # Установим параметры генератора, которые не будут меняться при выгрузке пачек данных
        self._query_builder_settings.limit = self._settings.batch_size
        self._query_builder_settings.where_conditions.extend([
            f"{self._settings.date_field_name} >= '{str(self._state.date_from)}'",
            f"{self._settings.date_field_name} < '{str(self._state.date_to)}'",
        ]
        )

        self._extract()
