import json

import redis

from models.state import EtlState
from utils import MyEncoder, json_parser, logger, on_exception

from .base import BaseStorageState


class RedisStorageState(BaseStorageState):
    def __init__(self, key: str, host: str, port: int, db: int = 0):
        self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.key = key

    @on_exception(redis.ConnectionError, logger)
    def save(self, state: EtlState) -> None:
        self._redis.set(self.key, json.dumps(state.dict(), cls=MyEncoder))

    @on_exception(redis.ConnectionError, logger)
    def retrieve(self) -> EtlState | None:
        result = None
        value = self._redis.get(self.key)
        if value:
            result = EtlState(**json.loads(value, object_hook=json_parser))
        return result
