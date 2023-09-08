import abc
import typing

from core import BaseLoaderSettings


class BaseLoaderBackend(abc.ABC):
    """Базовый класс загрузчиков."""
    def __init__(self, settings: BaseLoaderSettings) -> None:
        self._settings = settings

    @abc.abstractmethod
    def get_data(self) -> typing.Generator[typing.Any, None, None]:
        """Метод выборки загружаемых данных."""
        pass

    @abc.abstractmethod
    def load(self, data: typing.Any) -> None:
        """Метод загрузки данных в целевое хранилище."""
        pass
