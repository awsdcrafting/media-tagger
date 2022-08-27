from dataclasses import dataclass
from enum import Enum
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class NamingTargetType(Enum):
    TAG = 1
    TAG_CATEGORY = 2
    FILE_NAME = 3
    FOLDER_COUNT = 4
    GLOBAL_COUNT = 5


@dataclass_json
@dataclass
class NamingTarget:
    target_type: NamingTargetType
    target_names: (List[str] | str)
    deliminator: str
