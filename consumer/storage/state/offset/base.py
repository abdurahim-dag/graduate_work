import abc


class BaseStorage:
    @abc.abstractmethod
    def save(self, partition: int, offset: int) -> None:
        """Сохранить офсет партиции в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve(self, partition: int) -> int:
        """Загрузить офсет партиции локально из постоянного хранилища"""
        pass
