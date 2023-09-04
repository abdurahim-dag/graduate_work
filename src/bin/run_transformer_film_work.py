from transformers import JSONTransformer
from core import JSONTransformSettings
from core import Settings
from models import Movie
from states import RedisStorageState
import pathlib

if __name__=='__main__':
    settings = Settings()
    transformer_settings = JSONTransformSettings(
        dir_path=settings.data_dir_path,
    )
    storage_state = RedisStorageState(
        key='etl:transformer:film_work',
        host=settings.state_host,
        port=settings.state_port,
    )
    transformer = JSONTransformer(
        settings=transformer_settings,
        model=Movie,
    )
    transformer.run()
