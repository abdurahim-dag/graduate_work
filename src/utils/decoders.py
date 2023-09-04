import json
import re
import uuid
import typing
import datetime
import pendulum


def json_decoder(value):
    return json.loads(value.decode())


def decode_uuid(binary):
    return uuid.UUID(bytes=binary)


class MyEncoder(json.JSONEncoder):
    """JSONEncoder for date type."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


class MyDecoder(json.JSONDecoder):

    def default(self, dct):
        print("Edge(actor, movie)")
        return dct

def json_parser(dct):
    for k, v in dct.items():
        if isinstance(v, str):
            if re.search(r'-\d\dT\d\d:', v):
                dct[k] = pendulum.parse(v)
            elif re.compile(
                r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            ).match(v):
                dct[k] = uuid.UUID(v)
    return dct

