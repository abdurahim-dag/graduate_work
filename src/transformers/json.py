"""Модуль, для сложных специализированных запросов."""
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

class JSONTransformer:

    def __init__(
        self,
        settings: JSONTransformSettings,
        model: Type[BaseModel],
    ):
        """
        Инициализирует объект построителя SQL-запросов.

        Пример:
            sql_builder = SQLQueryBuilder(etl_settings)
        """
        self._settings = settings
        self._model: Type[BaseModel] = model


    def run(self):
        for src_file in pathlib.Path(self._settings.dir_path).glob(f"**/{self._settings.src_prefix_file}*.json"):
            correct: list[dict | None] = []
            incorrect: list[dict | None] = []

            with open(src_file, 'r', encoding='utf-8') as f:
                try:
                    rows = json.load(f, object_hook=json_parser)
                except Exception as err:
                    logger.exception(err)
                    continue
                for row in rows:
                    try:
                        # Чекаем данные по модели.
                        fields_value = dict()
                        for field in self._model.model_fields:
                            fields_value[field] = row[field]
                        model = self._model(**fields_value)
                        correct.append(model.model_dump(mode='json'))
                    # Если ошибка, то значит не соответствует модели.
                    except Exception as err:
                        logger.exception(err)
                        incorrect.append(row)

            correct_target_file = pathlib.PurePath(
                self._settings.dir_path,
                f"{self._settings.correct_prefix_file}{src_file.name}"
            )
            incorrect_target_file = pathlib.PurePath(
                self._settings.dir_path,
                f"{self._settings.incorrect_prefix_file}{src_file.name}"
            )

            if correct:
                with open(correct_target_file, 'w', encoding='utf-8') as f:
                    json.dump(correct, f, cls=MyEncoder, sort_keys=True, ensure_ascii=False)

            if incorrect:
                with open(incorrect_target_file, 'w', encoding='utf-8') as f:
                    json.dump(incorrect, f, cls=MyEncoder, sort_keys=True, ensure_ascii=False)

            os.remove(src_file)
