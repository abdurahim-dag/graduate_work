import os
import pathlib
from contextlib import closing

import elasticsearch as es

from utils import on_exception
from utils import logger
from core import ESLoaderSettings


class ESLoader:
    """Load to ES index."""
    def __init__(
            self,
            settings: ESLoaderSettings,
    ):
        self._settings = settings

    @on_exception(
        exception=es.exceptions.ElasticsearchException,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def run(self):
        """Load bulk batches rows to ES index."""
        self.client = es.Elasticsearch(
            self._settings.conn_params
        )

        for file_path in pathlib.Path(self._settings.dir_path).glob(f"**/{self._settings.src_prefix_file}-*.json"):
            with closing(open(file_path, 'r', encoding='utf-8')) as file:
                body = file.read()
                self.client.bulk(
                    index=self._settings.index_name,
                    body=body,
                )
                logger.info('%s loaded to ES!', file.name)
            os.remove(file_path)
