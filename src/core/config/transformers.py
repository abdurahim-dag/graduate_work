from pydantic import BaseModel
import dataclasses
import pathlib
from typing import List, Tuple, Optional


@dataclasses.dataclass
class TransformSettings:
    file_name: str
    file_path: pathlib.Path
    index_name: str
    schema: str = 'staging'

