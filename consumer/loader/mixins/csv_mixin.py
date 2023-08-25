import pydantic
from utils import logger


class CSVMixin:
    def _to_csv_line(self, model):
        # Приведём формат времени к нужному
        model.timestamp = model.timestamp.format('YYYY-MM-DD hh:mm:ss')
        return (
            ','.join([str(getattr(model, field, '')) for field in self._column_names])
            + '\n'
        )

    def _to_csv(self, elements: list[pydantic.BaseModel]):
        """Сохранение и проверка элементов."""
        with open(self._data_filename, 'wt') as csv:
            for element in elements:
                try:
                    csv.write(self._to_csv_line(element))
                except Exception as e:
                    # Все неправильные сообщения обрабатываем отдельно
                    logger.error(e)
