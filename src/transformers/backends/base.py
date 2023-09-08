import abc
import typing
import pydantic
from core import BaseTransformSettings


class BaseTransformerBackend(abc.ABC):
    def __init__(self, settings: BaseTransformSettings):
        self._settings = settings

    @abc.abstractmethod
    def get_models(self) -> typing.Generator[typing.List[pydantic.BaseModel], None, None]:
        """Метод выборки загружаемых данных."""
        pass


    @abc.abstractmethod
    def transform(self, models: typing.List[pydantic.BaseModel]) -> typing.List[pydantic.BaseModel]:
        """Метод трансформации загружаемых данных."""
        pass

    @abc.abstractmethod
    def load(self, model: typing.List[pydantic.BaseModel]) -> None:
        """Метод загрузки данных в целевое хранилище."""
        pass
