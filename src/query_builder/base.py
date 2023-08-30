import abc
from core import BaseExtractorSettings

class QueryBuilderBase(abc.ABC):

    @abc.abstractmethod
    def __init__(self, settings: BaseExtractorSettings):
        """Строит запрос."""
        pass


    @abc.abstractmethod
    def build_query(self) -> str:
        """Строит запрос."""
        pass
