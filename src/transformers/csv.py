"""Модуль, для сложных специализированных запросов."""
import sqlalchemy
import os
import re
import csv
from core import CSVTransformSettings
from pydantic import BaseModel
import sqlalchemy
import pathlib

class CSVTransformer:

    def __init__(
        self,
        settings: CSVTransformSettings,
        model: BaseModel,
    ):
        """
        Инициализирует объект построителя SQL-запросов.

        Пример:
            sql_builder = SQLQueryBuilder(etl_settings)
        """
        self._settings = settings
        self._model: BaseModel = model

    def transform(
            self,
    ):
        """Transform pg json formatted to ES format."""

    def run(self):
        for src_file in self._settings.src_dir_path.glob(f"**/{self._settings.src_prefix_file}-*.csv"):
            with open(src_file, 'r', encoding='utf-8') as f:
                rows = csv.DictReader(
                    f,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_ALL,
                    lineterminator='\n',
                )

            correct: list[BaseModel] = []
            incorrect: list[BaseModel] = []

            for row in rows:
                try:
                    # Чекаем данные по модели.
                    model = self._model(**row)
                    correct.append(model)
                # Если ошибка, то значит не соответствует модели.
                except Exception as err:
                    incorrect.append(row)

            correct_target_file = pathlib.PurePath(
                self._settings.dst_dir_path,
                re.sub(
                    self._settings.src_prefix_file,
                    self._settings.dst_prefix_file,
                    src_file.name
                )
            )
            incorrect_target_file = pathlib.PurePath(
                self._settings.dst_dir_path,
                re.sub(
                    self._settings.src_prefix_file,
                    self._settings.incorrect_prefix_file,
                    src_file.name
                )
            )

            with open(correct_target_file, 'w', encoding='utf-8') as f:
                csvwriter = csv.DictWriter(
                    f,
                    fieldnames=self._model.model_fields,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_ALL,
                    lineterminator='\n',
                )
                for model in correct:
                    csvwriter.writerow(model.model_dump())

            with open(incorrect_target_file, 'w', encoding='utf-8') as f:
                csvwriter = csv.DictWriter(
                    f,
                    fieldnames=self._model.model_fields,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_ALL,
                    lineterminator='\n',
                )
                for model in incorrect:
                    csvwriter.writerow(model.model_dump())

            os.remove(src_file)
