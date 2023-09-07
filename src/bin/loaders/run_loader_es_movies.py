import pathlib
import sys

from core import ESLoaderSettings
from loaders import ESLoader


es_host = sys.argv[1]
es_port = sys.argv[2]
dir_path = sys.argv[3]

if __name__=='__main__':

    for target in [
        ('movies', 'es-movies'),
        ('persons', 'es-persons'),
        ('genres', 'es-genres')
    ]:
        loader_settings = ESLoaderSettings(
            es_host=es_host,
            es_port=es_port,
            index_name=target[0],
            dir_path=pathlib.PurePath(dir_path),
            src_prefix_file=target[1]
        )
        loader = ESLoader(
            settings=loader_settings,
        )
        loader.run()
