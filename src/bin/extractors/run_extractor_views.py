import pathlib
import sys

from core import PostgresExtractorSettings
from core import SqlQueryBuilderSettings
from extractors import Extractor
from extractors.backend import PostgresExtractorBackend
from query_builder import SimpleSQLBuilder
from states import RedisStorageState


host = sys.argv[1]
port = sys.argv[2]
db = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
batch_size = sys.argv[6]
dir_path = sys.argv[7]
state_host = sys.argv[8]
state_port = sys.argv[9]

if __name__ == '__main__':
    for view in ['movies', 'persons', 'genres']:
        settings = PostgresExtractorSettings(
            host=host,
            port=int(port),
            dbname=db,
            username=username,
            password=password,
            batch_size=int(batch_size),
            dir_path=pathlib.PurePath(dir_path),
            filename_prefix='extract_view',
            schema='ods'
        )
        storage_state = RedisStorageState(
            key=f"etl:extractor:views:{view}", host=state_host, port=int(state_port)
        )

        backend = PostgresExtractorBackend(
            settings=settings,
            storage_state=storage_state,
            query_builder_type=SimpleSQLBuilder,
            query_builder_settings=SqlQueryBuilderSettings(
                source_type='postgres', source_name=f"v_{view}", schema=settings.schema
            ),
        )

        extractor = Extractor(backend=backend)
        extractor.run()
