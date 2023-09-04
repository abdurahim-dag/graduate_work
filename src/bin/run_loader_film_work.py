from loaders import PostgresStagingLoader
from core import PostgresStagingLoaderSettings
from core import Settings
from models import Movie
from states import RedisStorageState
import pathlib

if __name__=='__main__':
    settings = Settings()
    loader_settings = PostgresStagingLoaderSettings(
        host=settings.staging_host,
        port=settings.staging_port,
        dbname=settings.staging_dbname,
        username=settings.staging_username,
        password=settings.staging_password,
        batch_size=settings.batch_size,
        dir_path=settings.data_dir_path,
        src_prefix_file='correct-transformed'
    )
    loader = PostgresStagingLoader(
        settings=loader_settings,
        model=Movie,
    )
    loader.run()
