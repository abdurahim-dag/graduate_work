import json
import os
import pathlib
import re
import typing
from pathlib import PurePath

import pydantic

from core import ESTransformSettings
from models.es import ESIndex
from models.es import ESIndexLine
from utils import MyEncoder
from utils import logger
from .base import BaseTransformerBackend


class ESTransformerBackend(BaseTransformerBackend):
    """Transform pg json formatted to ES format."""
    def __init__(self, settings: ESTransformSettings):
        super().__init__(settings)
        self._src_file_name = None

    def get_models(self) -> typing.Generator[typing.List[pydantic.BaseModel], None, None]:
        for src_file in pathlib.Path(self._settings.dir_path).glob(
                f"**/{self._settings.src_filename_prefix}-*.json"
        ):
            with open(src_file, encoding='utf-8') as file:
                src_json = json.load(file)
            logger.info(f"loaded - {src_file}")
            models = []
            for row in src_json:
                try:
                    model = self._settings.model(**row['obj'])
                    models.append(model)
                # Если ошибка, то значит не соответствует модели.
                except Exception as err:
                    logger.info("Error on check transform file %s", src_file)
                    raise err
            self._src_file_name = file.name
            yield models

            os.remove(src_file)
            logger.info(f"removed file - {str(src_file)}")


    def transform(self, models: typing.List[pydantic.BaseModel]) -> typing.List[pydantic.BaseModel]:
        results = []
        for model in models:
            es_index = ESIndex(_id=model.id, _index=self._settings.index_name)
            index_line = ESIndexLine(index=es_index)
            results.append(index_line)
            results.append(model)
        return results


    def load(self, models: typing.List[pydantic.BaseModel]) -> None:
        file_name = re.search(
            f"{self._settings.src_filename_prefix}-(.*).json",
            self._src_file_name
        ).group(1)
        target_file_path = PurePath(
            self._settings.dir_path,
            f"es-{self._settings.index_name}-{file_name}.json",
        )
        logger.info(f"target file - {str(target_file_path)}")
        with open(target_file_path, 'w', encoding='utf-8') as file:
            for model in models:
                json.dump(model.model_dump(by_alias=True), file, cls=MyEncoder)
            file.write('\n')
