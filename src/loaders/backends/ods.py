"""Загрузчик в центральный слой."""
import json
import os
import pathlib
from .base import BaseLoaderBackend
import dataclasses
import sqlalchemy
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.orm import Session
from typing import Generator
from core import ODSLoaderSettings
from models.ods import Base, DLQ
from utils import json_parser, logger, on_exception
from .dead_letter_queue import DLQLoaderBackend


class ODSLoaderBackend(BaseLoaderBackend):
    """Postgres loader."""
    def __init__(self, settings: ODSLoaderSettings) -> None:
        super().__init__(settings)
        self._dlq_loader = DLQLoaderBackend(
            settings=dataclasses.replace(
                settings,
                model=DLQ,
            )
        )

    def _model_to_dict(self, model: Base) -> dict:
        model_dict = dict()
        columns = [col.name for col in list(self._settings.model.__table__.columns)]
        for column in columns:
            model_dict[column] = getattr(model, column)
        return model_dict


    def get_data(self) -> Generator[list[Base], None, None]:
        """Выборка данных из файла."""
        for src_file in pathlib.Path(self._settings.dir_path).glob(
                f"**/{self._settings.src_prefix_file}-*.json"
        ):
            models: list[Base | None] = []
            columns = [col.name for col in list(self._settings.model.__table__.columns)]

            with open(src_file, encoding='utf-8') as f:
                rows = json.load(f, object_hook=json_parser)
                for row in rows:
                    fields_value = dict()
                    for column in columns:
                        fields_value[column] = row.get(column, None)
                    model = self._settings.model(**fields_value)
                    models.append(model)
            yield models
            os.remove(src_file)

    @on_exception(
        exception=OperationalError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def load(self, models: list[Base | None]) -> None:
        """Загрузка данных в Postgres."""
        engine = sqlalchemy.create_engine(self._settings.conn_str)
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
                    self._dlq_loader.load(
                        {
                            "obj": self._model_to_dict(model),
                            "description": str(err)
                        }
                    )
