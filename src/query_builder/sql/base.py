import abc


class QueryBuilderBase(abc.ABC):

    @abc.abstractmethod
    def build_query(self) -> str:
        """Строит запрос."""
        pass
