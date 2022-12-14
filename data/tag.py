from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Tag:
    name: str
    category: str
    id: int = -1
