from extractors import PostgresExtractor
from core import PostgresExtractorSettings
from core import SqlQueryBuilderSettings
from core import Settings
from states import RedisStorageState
from query_builder import SimpleSQLQueryBuilder

if __name__=='__main__':
    settings = Settings()
    extractor_settings = PostgresExtractorSettings(
        host=settings.movies_host,
        port=settings.movies_port,
        dbname=settings.movies_dbname,
        username=settings.movies_username,
        password=settings.movies_password,
        batch_size=settings.batch_size,
    )
    storage_state = RedisStorageState(
        key='etl:extractor:film_work',
        host=settings.state_host,
        port=settings.state_port,
    )

    extractor = PostgresExtractor(
        settings=extractor_settings,
        storage_state=storage_state,
        query_builder_type=SimpleSQLQueryBuilder,
        query_builder_settings=SqlQueryBuilderSettings(
            source_type='postgres',
            source_name='film_work',
            dbschema='content'
        ),
        extract_dir_path=settings.extract_dir_path
    )

    extractor.run()
