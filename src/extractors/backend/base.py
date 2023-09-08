import abc
import typing

from core import BaseExtractorSettings


class BaseExtractorBackend(abc.ABC):
    """Базовый класс загрузчиков."""
    def __init__(self, settings: BaseExtractorSettings) -> None:
        self._settings = settings

    @abc.abstractmethod
    def get_data(self) -> typing.Generator[typing.List, None, None]:
        """Метод выборки загружаемых данных."""
        pass

    @abc.abstractmethod
    def save(self, data: typing.List) -> None:
        """Метод загрузки данных в целевое хранилище."""
        pass
