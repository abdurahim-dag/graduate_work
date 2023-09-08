import pathlib
import sys

from core import ESLoaderSettings
from loaders import Loader
from loaders.backends import ESLoaderBackend

host = sys.argv[1]
port = sys.argv[2]
dir_path = sys.argv[3]

if __name__ == '__main__':
    for target in [
        ('movies', 'es-movies'),
        ('persons', 'es-persons'),
        ('genres', 'es-genres'),
    ]:
        settings = ESLoaderSettings(
            host=host,
            port=int(port),
            index_name=target[0],
            dir_path=pathlib.PurePath(dir_path),
            src_prefix_file=target[1],
            model=None,
        )
        backend = ESLoaderBackend(settings=settings)
        loader = Loader(backend=backend)
        loader.run()
