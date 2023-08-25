import time

import loader
import pydantic
import storage
from utils import logger

from core import Settings


def run(
    name: str,
    settings: Settings,
    loader: type[loader.BaseLoader],
    model: type[pydantic.BaseModel],
    data_filename: str,
    key_statestorage: str,
    state_defvalue: dict,
    collection: str,
    write_tabelname: str,
):
    loader = loader(
        model=model,
        data_filename=data_filename,
        settings=settings,
        state_storage=storage.state.RedisState(
            key=key_statestorage,
            def_value=state_defvalue,
            host=settings.redis_host,
            port=settings.redis_port,
        ),
        reader=storage.readers.MongoReader(
            storage.readers.MongoConnect(
                host=settings.mongo_host,
                port=settings.mongo_port,
                user=settings.mongo_user,
                pw=settings.mongo_password,
                rs=settings.mongo_rs,
                auth_db=settings.mongo_authdb,
                main_db=settings.mongo_db,
                cert_path=settings.mongo_certpath,
            ),
            collection=collection,
        ),
        writer=storage.writers.ClickhouseWriter(
            host=settings.ch_host,
            port=settings.ch_port,
            username=settings.ch_username,
            password=settings.ch_password,
            db=settings.ch_db,
            table=write_tabelname,
            model=model,
        ),
        logger=logger,
    )

    while True:
        try:
            processed = loader.load()
            if processed == 0:
                logger.warning(f"No docs for ETL {name}, to sleep")
                time.sleep(5)

        except KeyboardInterrupt:
            logger.warning('Quit')
            break
