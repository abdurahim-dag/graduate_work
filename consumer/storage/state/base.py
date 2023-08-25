import abc


class BaseState:
    @abc.abstractmethod
    def save(self, state: dict) -> None:
        """Сохранить офсет партиции в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve(self) -> dict:
        """Загрузить офсет партиции локально из постоянного хранилища"""
        pass
