import json
from psycopg.rows import dict_row
from pydantic import BaseModel
import pendulum
import psycopg
import pathlib
from utils import on_exception
from utils import logger
from utils import MyEncoder
from core import PostgresStagingLoaderSettings
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from states import BaseStorageState
from sqlalchemy.dialects.postgresql import insert
from typing import Type
from models.staging import Base
import sqlalchemy
import os
import re
import json
from core import JSONTransformSettings
from pydantic import BaseModel
import sqlalchemy
import pathlib
from typing import Type
from utils import logger
from utils import json_parser
from utils import MyEncoder




class PostgresStagingLoader:
    """Extract batches rows to files."""
    def __init__(
            self,
            settings: PostgresStagingLoaderSettings,
            model: Type[Base],
    ) -> None:
        self._settings = settings
        self._model = model

    @on_exception(
        exception=OperationalError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def _load(self, models: list[Base | None]):
        engine = sqlalchemy.create_engine(self._settings.conn_params)
        with Session(engine) as session:
            for model in models:
                try:
                    session.merge(model)
                    session.commit()
                except Exception as err:
                    session.rollback()
                    raise err


    def run(self):
        for src_file in pathlib.Path(self._settings.dir_path).glob(f"**/{self._settings.src_prefix_file}*.json"):
            models: list[Base | None] = []

            with open(src_file, 'r', encoding='utf-8') as f:
                rows = json.load(f, object_hook=json_parser)
                for row in rows:
                    model = self._model(**row)
                    models.append(model)

            self._load(models)
            os.remove(src_file)