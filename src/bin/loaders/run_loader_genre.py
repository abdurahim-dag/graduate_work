import pathlib
import sys

from core import PostgresStagingLoaderSettings
from loaders import PostgresStagingLoader
from models.staging import Genre


host = sys.argv[1]
port = sys.argv[2]
dbname = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
batch_size = sys.argv[6]
dir_path = sys.argv[7]

if __name__=='__main__':

    loader_settings = PostgresStagingLoaderSettings(
        host=host,
        port=int(port),
        dbname=dbname,
        username=username,
        password=password,
        batch_size=int(batch_size),
        dir_path=pathlib.PurePath(dir_path),
        src_prefix_file='correct-transformed-extract-genre-'
    )
    loader = PostgresStagingLoader(
        settings=loader_settings,
        model=Genre,
    )
    loader.run()
