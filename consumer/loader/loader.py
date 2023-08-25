from .base import BaseLoader
from .mixins.csv_mixin import CSVMixin


class Loader(BaseLoader, CSVMixin):
    def load(self):
        state = self._state_storage.retrieve()
        last_loaded = state['timestamp']

        load_queue = self._reader.get(
            field_threshold='timestamp',
            load_threshold=last_loaded,
            limit=state['limit'],
            skip=state['skip'],
        )

        models = []
        for doc in load_queue:
            model = self._get_validated({k: str(v) for k, v in doc.items()})
            if model:
                models.append(model)

        if models:
            self._to_csv(models)
            self._writer.save(self._data_filename)

            self._logger.info(f"Found {len(models)} models to load.")

        state['skip'] += state['limit']
        state['timestamp'] = last_loaded
        self._state_storage.save(state)

        return len(load_queue)
