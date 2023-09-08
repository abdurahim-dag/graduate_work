import dataclasses
import pathlib
import pydantic


@dataclasses.dataclass
class BaseTransformSettings:
    dir_path: pathlib.PurePath
    src_filename_prefix: str

@dataclasses.dataclass
class ESTransformSettings(BaseTransformSettings):
    index_name: str
    model: pydantic.BaseModel
