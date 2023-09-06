import json
import os
import pathlib

import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from core.config import PostgresStagingLoaderSettings
from models.staging import Base
from models.staging import DLQ
from utils import json_parser
from utils import logger
from utils import on_exception


class DLQLoader:

    def __init__(
            self,
            settings: PostgresStagingLoaderSettings,
    ) -> None:
        self._settings = settings

    @on_exception(
        exception=OperationalError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def _load(self, model: DLQ):
        engine = sqlalchemy.create_engine(self._settings.conn_params)
        with Session(engine) as session:
            try:
                session.add(model)
                session.commit()
            except Exception as err:
                session.rollback()
                raise err

    def load(self, value: dict, description: str):
        self._load(DLQ(
            obj=json.dumps(value),
            description=description
        ))

    def ru