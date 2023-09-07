import abc

from core import BaseQueryBuilderSettings


class QueryBuilderBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, settings: BaseQueryBuilderSettings):
        """Строит запрос."""
        pass

    @abc.abstractmethod
    def build_query(self) -> str:
        """Строит запрос."""
        pass
