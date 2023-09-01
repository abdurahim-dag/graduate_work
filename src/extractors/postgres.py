import json
import csv
from contextlib import closing
from pathlib import PurePath, Path

import psycopg

from utils import on_exception
from utils import logger
from core import PostgresExtractorSettings, SqlQueryBuilderSettings

from states import BaseState
from query_builder import QueryBuilderBase
from typing import Type
from models import EtlState

class PostgresExtractor:
    """Extract batches rows to files."""
    def __init__(
            self,
            settings: PostgresExtractorSettings,
            storage_state: BaseState,
            query_builder_type: Type[QueryBuilderBase],
            query_builder_settings: SqlQueryBuilderSettings,
            extract_dir_path: PurePath,

    ) -> None:
        self._settings = settings
        self._storage_state = storage_state
        self._query_builder_type = query_builder_type
        self._query_builder_settings = query_builder_settings
        self._extract_dir_path = extract_dir_path


    def _get_filname(self, name: str, date: str, offset: str) -> str:
        return f"{name}-{date}-{offset}.csv"

    def _get_filepath(self, name: str, date: str, offset: str) -> str:
        file_name = self._get_filname(
            name=name,
            date=date,
            offset=offset
        )
        return str(self._extract_dir_path / file_name)


    @on_exception(
        exception=psycopg.DatabaseError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def extract(self):
        """Extract rows to files."""
        with psycopg.connect(**self._settings.conn_params()) as conn:
            with conn.cursor() as curs:

                state: EtlState = self._storage_state.retrieve()
                if state is None:
                    state = EtlState()

                self._settings.where_conditions = [
                    f"modified >= {str(state.date_from)}",
                    f"modified < {str(state.date_to)}",
                ]
                state.offset

                while True:
                    sql = self._query_builder_type(settings=self._query_builder_settings).build_query()

                    curs.execute(sql)

                    rows = curs.fetchmany()
                    if len(rows) == 0:
                        break

                    file_path = self._get_filepath(
                        name=self._settings.source_name,
                        date=str(state.date_from),
                        offset=str(state.offset)
                    )

                    with open(file_path, 'w', encoding='utf-8') as f:
                        csvwriter = csv.writer(
                            f,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL
                        )
                        csvwriter.writerow(rows)

                    # Сохраняем каждый выполненный шаг.
                    state.offset += state.
                    self._storage_state.save(state)
                    logger.info("Extracted file %s", file_path)

                # Сохраним step < 0.
                # Установим дату началу, следующего запуска со вчера.
                # И следующий запуск начнётся со вчерашней даты.
                state.step = -1
                state.date_from = state.date_to
                self._storage_state.save(state)
