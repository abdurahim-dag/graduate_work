from .backends import BaseLoaderBackend

class Loader:
    def __init__(self, backend: BaseLoaderBackend):
        self._backend = backend

    def run(self):
        for data in self._backend.get_data():
            self._backend.load(data)
