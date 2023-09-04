from pydantic import BaseModel
import dataclasses
import pathlib
from typing import List, Tuple, Optional


@dataclasses.dataclass
class CSVTransformSettings:
    src_dir_path: pathlib.Path
    dst_dir_path: pathlib.Path
    src_prefix_file: str = 'extract'
    dst_prefix_file: str = 'transformed'
    incorrect_prefix_file: str = 'incorrect-transformed'
