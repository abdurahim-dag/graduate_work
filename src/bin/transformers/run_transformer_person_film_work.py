from core import JSONTransformSettings
from core import Settings
from models.movies import PersonFilmWork
from transformers import JSONTransformer


if __name__=='__main__':
    settings = Settings()
    transformer_settings = JSONTransformSettings(
        src_prefix_file='extract-person_film_work-',
        dir_path=settings.data_dir_path,
    )
    transformer = JSONTransformer(
        settings=transformer_settings,
        model=PersonFilmWork,
    )
    transformer.run()
