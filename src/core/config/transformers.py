from pydantic import BaseModel
import dataclasses
import pathlib
from typing import List, Tuple, Optional


@dataclasses.dataclass
class JSONTransformSettings:
    dir_path: pathlib.PurePath
    src_prefix_file: str = 'extract'
    correct_prefix_file: str = 'correct-transformed'
    incorrect_prefix_file: str = 'incorrect-transformed'
