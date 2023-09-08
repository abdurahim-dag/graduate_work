from .backends import BaseTransformerBackend

class Transformer:
    def __init__(self, backend: BaseTransformerBackend):
        self._backend = backend

    def run(self):
        for models in self._backend.get_models():
            transformed_models = self._backend.transform(models)
            self._backend.load(transformed_models)
