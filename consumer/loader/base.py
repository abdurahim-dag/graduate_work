import abc

import pydantic
import storage


class BaseLoader(metaclass=abc.ABCMeta):
    def __init__(
        self,
        model: type[pydantic.BaseModel],
        data_filename: str,
        settings: pydantic.BaseSettings,
        state_storage: storage.state.BaseState,
        reader: storage.readers.BaseReader,
        writer: storage.writers.BaseWriter,
        threshold_field: str,
        threshold_offset: int,
        threshold_limit: int,
        logger,
    ):
        self._model = model
        self._column_names = tuple(model.__fields__.keys())
        self._data_filename = data_filename
        self._settings = settings
        self._state_storage = state_storage
        self._model = model
        self._column_names = tuple(model.__fields__.keys())
        self._reader = reader
        self._writer = writer
        self._threshold_field = threshold_field
        self._threshold_offset = threshold_offset
        self._threshold_limit = threshold_limit

        self._logger = logger

    def _to_deadletter_queue(self, value):
        self._logger.error('Exception on message to model: %s', (str(value),))

    def _get_validated(self, value: dict) -> pydantic.BaseModel | None:
        model = None
        try:
            model = self._model(**value)
        except Exception as e:
            self._to_deadletter_queue(value)
            self._logger.error(e)
        return model

    @abc.abstractmethod
    def load(self):
        pass
