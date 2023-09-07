"""Загрузчик в центральный слой."""
import json
import os
import pathlib
from typing import Type

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from core import PostgresODSLoaderSettings
from models.ods import Base
from utils import json_parser
from utils import logger
from utils import on_exception
from .dead_letter_queue import DLQLoader


class PostgresODSLoader:
    def __init__(
            self,
            settings: PostgresODSLoaderSettings,
            model: Type[Base],
    ) -> None:
        self._settings = settings
        self._model = model
        self._dlq = DLQLoader(settings=settings)

    def _model_to_dict(self, model: Base) -> dict:
        model_dict = dict()
        columns = [col.name for col in list(self._model.__table__.columns)]
        for column in columns:
            model_dict[column] = getattr(model, column)
        return model_dict

    @on_exception(
        exception=OperationalError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def _load(self, models: list[Base | None]):
        engine = sqlalchemy.create_engine(
            self._settings.conn_params
        )
        with Session(engine) as session:
            for model in models:
                try:
                    session.merge(model)
                    session.commit()

                # ProgrammingError - не соответствия типа столбцов
                # IntegrityError - ссылочная целостность
                except (ProgrammingError, IntegrityError) as err:
                    logger.exception(err)
                    session.rollback()
                    self._dlq.load(self._model_to_dict(model), str(err))

    def run(self):
        for src_file in pathlib.Path(self._settings.dir_path).glob(f"**/{self._settings.src_prefix_file}*.json"):
            models: list[Base | None] = []
            columns = [col.name for col in list(self._model.__table__.columns)]

            with open(src_file, 'r', encoding='utf-8') as f:
                rows = json.load(f, object_hook=json_parser)
                for row in rows:
                    fields_value = dict()
                    for column in columns:
                        fields_value[column] = row.get(column, None)
                    model = self._model(**fields_value)
                    models.append(model)

            self._load(models)
            os.remove(src_file)
