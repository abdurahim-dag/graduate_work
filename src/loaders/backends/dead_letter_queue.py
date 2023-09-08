"""Загрузчик в таблицу информации об ошибках импорта объектов."""
import json

import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from utils import MyEncoder
from core.config import ODSLoaderSettings
from utils import logger
from utils import on_exception
from .base import BaseLoaderBackend
from models.ods import DLQ


class DLQLoaderBackend(BaseLoaderBackend):
    """Dead letter queue loader."""
    def __init__(self, settings: ODSLoaderSettings) -> None:
        super().__init__(settings)
        self._engine = None
        self._session = None

    def _set_session(self):
        self._engine = sqlalchemy.create_engine(self._settings.conn_str)
        self._session = Session(self._engine)

    @on_exception(
        exception=OperationalError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def _load(self, model: DLQ):
        if self._session is None:
            self._set_session()

        with self._session:
            try:
                self._session.add(model)
                self._session.commit()
            except OperationalError as err:
                self._session = None
                raise err


    def load(self, data: dict):
        model = DLQ(
            obj=json.dumps(
                data['obj'],
                cls=MyEncoder,
                sort_keys=True,
                ensure_ascii=False
            ),
            description=data['description'],
        )
        self._load(model)
