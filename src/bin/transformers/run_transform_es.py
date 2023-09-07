import pathlib
import sys

from core import TransformSettings
from models.es import Movie, Genre, Person
from transformers import ESTransform


dir_path = sys.argv[1]

if __name__=='__main__':
    for target in [
        ('extract_view-v_persons', 'persons', Person),
        ('extract_view-v_genres', 'genres', Genre),
        ('extract_view-v_movies', 'movies', Movie)
    ]:
        transformer_settings = TransformSettings(
            dir_path=pathlib.PurePath(dir_path),
            index_name=target[1],
            model=target[2],
            src_filename_prefix=target[0],
        )
        transformer = ESTransform(
            settings=transformer_settings,
        )
        transformer.run()