"""Модуль, для сложных специализированных запросов."""
import sqlalchemy

from core import Transform as TransformSettings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
import sqlalchemy


class Transformer:

    def __init__(
        self,
        settings: TransformSettings,
        model: DeclarativeBase,
        session: Session
    ):
        """
        Инициализирует объект построителя SQL-запросов.

        Пример:
            sql_builder = SQLQueryBuilder(etl_settings)
        """
        self._settings = settings
        self._model = model
        self._session = session


    def build_query(self) -> str:
        stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
        sqlalchemy.select()