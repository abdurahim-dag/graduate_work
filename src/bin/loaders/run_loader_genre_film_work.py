import pathlib
import sys

from core import PostgresODSLoaderSettings
from loaders import PostgresODSLoader
from models.ods import GenreFilmWork


host = sys.argv[1]
port = sys.argv[2]
dbname = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
batch_size = sys.argv[6]
dir_path = sys.argv[7]

if __name__=='__main__':

    loader_settings = PostgresODSLoaderSettings(
        host=host,
        port=int(port),
        dbname=dbname,
        username=username,
        password=password,
        batch_size=int(batch_size),
        dir_path=pathlib.PurePath(dir_path),
        src_prefix_file='extract-genre_film_work-'
    )
    loader = PostgresODSLoader(
        settings=loader_settings,
        model=GenreFilmWork,
    )
    loader.run()
