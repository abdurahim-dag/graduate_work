import dataclasses
import pathlib
import typing


@dataclasses.dataclass
class TransformSettings:
    dir_path: pathlib.PurePath
    index_name: str
    model: typing.Any
    src_filename_prefix: str
