import json
import os
import pathlib
import re
from pathlib import PurePath

from core import TransformSettings
from models.es import ESIndex, ESIndexLine
from utils import MyEncoder, logger


class ESTransform:
    def __init__(self, settings: TransformSettings):
        self._settings = settings

    def run(self):
        """Transform pg json formatted to ES format."""
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

            target_file_name = re.search(
                f"{self._settings.src_filename_prefix}-(.*).json", src_file.name
            ).group(1)
            target_file_path = PurePath(
                self._settings.dir_path,
                f"es-{self._settings.index_name}-{target_file_name}.json",
            )
            logger.info(f"target file - {str(target_file_path)}")
            with open(target_file_path, 'w', encoding='utf-8') as file:
                for model in models:
                    es_index = ESIndex(_id=model.id, _index=self._settings.index_name)
                    index_line = ESIndexLine(index=es_index)
                    json.dump(index_line.model_dump(by_alias=True), file, cls=MyEncoder)
                    file.write('\n')
                    json.dump(model.model_dump(), file, cls=MyEncoder)
                    file.write('\n')

            os.remove(src_file)
            logger.info(f"removed file - {str(src_file)}")
