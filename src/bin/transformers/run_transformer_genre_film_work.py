import pathlib
import sys

from core import JSONTransformSettings
from models.movies import GenreFilmWork
from transformers import JSONTransformer


dir_path = sys.argv[1]

if __name__=='__main__':
    transformer_settings = JSONTransformSettings(
        src_prefix_file='extract-genre_film_work-',
        dir_path=pathlib.PurePath(dir_path),
    )
    transformer = JSONTransformer(
        settings=transformer_settings,
        model=GenreFilmWork,
    )
    transformer.run()
