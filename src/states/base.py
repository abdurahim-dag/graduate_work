import abc
from models.state import EtlState

class BaseStorageState:
    @abc.abstractmethod
    def save(self, state: EtlState) -> None:
        """Сохранить офсет партиции в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve(self) -> EtlState | None:
        """Загрузить офсет партиции локально из постоянного хранилища"""
        pass
