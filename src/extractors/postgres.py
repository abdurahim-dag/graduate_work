import json
import csv
from contextlib import closing
from pathlib import PurePath, Path

import psycopg

from utils import on_exception
from utils import logger
from core import PostgresExtractorSettings
from states import BaseState
from query_builder import QueryBuilderBase
from typing import Type

class PostgresExtractor:
    """Extract batches rows to files."""
    def __init__(
            self,
            settings: PostgresExtractorSettings,
            storage_state: BaseState,
            query_builder: Type[QueryBuilderBase],
            file_path: Path,

    ) -> None:
        self._settings = settings
        self._storage_state = storage_state
        self._query_builder = query_builder
        self._file_path = file_path


    def _get_filname(self, name: str, date: str, step: str) -> str:
        return f"{name}-{date}-{step}.csv"

    def _get_filepath(self, name: str, date: str, step: str) -> str:
        file_name = self._get_filname(
            name=name,
            date=date,
            step=step
        )
        return str(PurePath(self._file_path, file_name))



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

                state = self._storage_state.retrieve()
                self._settings.where_conditions = ..
                sql = self._query_builder(settings=self._settings).build_query()

                curs.execute(sql)

                while rows := curs.fetchmany(self._settings.batch_size):
                    if len(rows) == 0:
                        break

                    file_path = self._get_filepath(
                        name=self._settings.source_name,
                        date=str(state.date_from),
                        step=str(state.step)
                    )

                    with open(file_path, 'w', encoding='utf-8') as f:
                        csvwriter = csv.writer(
                            f,
                            delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL
                        )
                        csvwriter.writerow(rows)

                    # Сохраняем каждый выполненный шаг.
                    state.step += 1
                    self._storage_state.save(state)
                    logger.info("Extracted file %s", file_path)

                # Сохраним step < 0.
                # Установим дату началу, следующего запуска со вчера.
                # И следующий запуск начнётся со вчерашней даты.
                state.step = -1
                state.date_from = state.date_to
                self._storage_state.save(state)
