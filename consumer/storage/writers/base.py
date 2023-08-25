import abc


class BaseWriter:
    @abc.abstractmethod
    def save(self, data_filepath: str) -> None:
        """Метод загрузки файла данных в БД.

        Args:
            data_filepath: Путь до файла данных загружаемого в БД.
        """
