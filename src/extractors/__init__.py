from .backend import BaseExtractorBackend


class Extractor:
    def __init__(self, backend: BaseExtractorBackend):
        self._backend = backend

    def run(self):
        for data in self._backend.get_data():
            self._backend.save(data)
