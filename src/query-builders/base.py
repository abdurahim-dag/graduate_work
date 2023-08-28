import abc
import datetime

class QueryBuilderBase(abc.ABC):

    @abc.abstractmethod
    def get(self) -> str:
        """Возвращает запрос."""
        pass
