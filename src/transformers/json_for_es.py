import json
import os
import pathlib
from pathlib import PurePath

from core import ESLoaderSettings
from models.es import ESIndex
from models.es import ESIndexLine
from utils import MyEncoder
from utils import logger


class ESTransform:

    def __init__(
            self,
            settings: ESLoaderSettings,
    ):
        self._settings = settings

    def transform(
            self,
    ):
        """Transform pg json formatted to ES format."""
        for src_file in pathlib.Path(self._settings.dir_path).glob(f"**/{self._settings.src_prefix_file}-*.json"):
            with open(src_file, 'r', encoding='utf-8') as file:
                src_json = json.load(file)
            models = []
            for row in src_json:
                try:
                    # Чекаем данные по модели.
                    model = self._settings.model(**row[0])
                    models.append(model)
                # Если ошибка, то значит не соответствует модели.
                except Exception as err:
                    logger.info("Error on check transform file %s", src_file)
                    raise err

            target_file = PurePath(self._settings.dir_path, src_file.name)
            with open(target_file, 'w', encoding='utf-8') as file:
                for model in models:
                    es_index = ESIndex(
                        _id=model.id,
                        _index=self._settings.index_name
                    )
                    index_line = ESIndexLine(
                        index=es_index
                    )
                    json.dump(index_line.dict(by_alias=True), file, cls=MyEncoder)
                    file.write('\n')
                    json.dump(model.dict(), file, cls=MyEncoder)
                    file.write('\n')

            os.remove(src_file)
