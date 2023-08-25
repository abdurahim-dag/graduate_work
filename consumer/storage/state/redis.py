import json

import redis
from utils import MyEncoder, json_parser, logger, on_exception

from .base import BaseState


class RedisState(BaseState):
    def __init__(self, key: str, def_value: dict, host: str, port: int, db: int = 0):
        self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.key = key
        self._def_value = def_value

    @on_exception(redis.ConnectionError, logger)
    def save(self, state: dict) -> None:
        self._redis.set(self.key, json.dumps(state, cls=MyEncoder))

    @on_exception(redis.ConnectionError, logger)
    def retrieve(self) -> dict:
        result = self._def_value
        value = self._redis.get(self.key)
        if value:
            result = json.loads(value, object_hook=json_parser)
        return result
