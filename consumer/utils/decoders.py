import json
import re
import uuid

import pendulum


def json_decoder(value):
    return json.loads(value.decode())


def decode_uuid(binary):
    return uuid.UUID(bytes=binary)


class MyEncoder(json.JSONEncoder):
    """JSONEncoder for date type."""

    def default(self, obj):
        if isinstance(obj, pendulum.DateTime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def json_parser(dct):
    for k, v in dct.items():
        if isinstance(v, str) and re.search(r'-\d\dT\d\d:', v):
            dct[k] = pendulum.parse(v)
    return dct
