from extractors import PostgresExtractor
from core import PostgresExtractorSettings
from core import Settings
from states import RedisState
from query_builder import SimpleSQLQueryBuilder

if __name__=='main':
    settings = Settings()
    extractor_settings = PostgresExtractorSettings(
        source_type='postgres',
        source_name='film_work',
        host=settings.movies_host,
        port=settings.movies_port,
        dbname=settings.movies_dbname,
        username=settings.movies_username,
        password=settings.movies_password,
        limit=settings.batch_size,
    )
    storage_state = RedisState(
        'etl:extractor:film_work',
        host=settings.redis_host,
        port=settings.redis_port,
    )

    extractor = PostgresExtractor(
        settings=extractor_settings,
        storage_state=storage_state,
        query_builder=SimpleSQLQueryBuilder,
        extract_dir_path=settings.extract_dir_path
    )

    extractor.extract()
