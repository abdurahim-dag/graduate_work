import abc
import datetime


class BaseReader:
    @abc.abstractmethod
    def get(
        self,
        field_threshold: str,
        load_threshold: datetime.datetime,
        limit: int,
        skip: int,
    ) -> list[dict]:
        """Метод чтения батча записей.

        Args:
            field_threshold: имя поля используемого в качестве смещения.
            load_threshold: значение смещения.
            limit: количество записей.
            skip: количество пропускаемых записей.

        Returns:
            Список считанных записей в виде словаря.
        """
        pass
