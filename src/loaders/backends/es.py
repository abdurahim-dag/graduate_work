"""Загрузчик в ES."""
import os
import pathlib
import typing

import elasticsearch as es

from utils import logger
from utils import on_exception
from .base import BaseLoaderBackend
from core import ESLoaderSettings

class ESLoaderBackend(BaseLoaderBackend):
    """Loader to ES index."""
    def __init__(self, settings: ESLoaderSettings):
        super().__init__(settings)
        self._client = None

    def _set_client(self):
        self._client = es.Elasticsearch(self._settings.conn_str)

    def get_data(self) -> typing.Generator[typing.AnyStr, None, None]:
        """Load bulk batches rows to ES index."""
        for file_path in pathlib.Path(self._settings.dir_path).glob(
            f"**/{self._settings.src_prefix_file}-*.json"
        ):
            with open(file_path, encoding='utf-8') as file:
                body = file.read()

            yield body

            logger.info('%s loaded to ES!', file_path.name)
            os.remove(file_path)

    @on_exception(
        exception=es.exceptions.ElasticsearchException,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def load(self, body: typing.AnyStr) -> None:
        """Загрузчик данных в индекс ES. На случай ошибки при подключении или загрузки повесили декоратор"""
        if self._client is None:
            self._set_client()
        self._client.bulk(index=self._settings.index_name, body=body)
