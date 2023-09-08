import pathlib
import sys

from core import ODSLoaderSettings
from loaders import Loader
from loaders.backends import ODSLoaderBackend
from models.ods import FilmWork


host = sys.argv[1]
port = sys.argv[2]
dbname = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
batch_size = sys.argv[6]
dir_path = sys.argv[7]

if __name__ == '__main__':
    settings = ODSLoaderSettings(
        host=host,
        port=int(port),
        dbname=dbname,
        username=username,
        password=password,
        batch_size=int(batch_size),
        dir_path=pathlib.PurePath(dir_path),
        src_prefix_file='extract-film_work',
        model=FilmWork
    )
    backend = ODSLoaderBackend(settings=settings)
    loader = Loader(backend=backend)
    loader.run()
