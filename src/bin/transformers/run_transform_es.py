import pathlib
import sys

from core import ESTransformSettings
from models.es import Genre, Movie, Person
from transformers import Transformer
from transformers.backends import ESTransformerBackend

dir_path = sys.argv[1]

if __name__ == '__main__':
    for target in [
        ('extract_view-v_persons', 'persons', Person),
        ('extract_view-v_genres', 'genres', Genre),
        ('extract_view-v_movies', 'movies', Movie),
    ]:
        settings = ESTransformSettings(
            dir_path=pathlib.PurePath(dir_path),
            src_filename_prefix=target[0],
            index_name=target[1],
            model=target[2]
        )
        backend = ESTransformerBackend(settings=settings)
        transformer = Transformer(backend=backend)
        transformer.run()
