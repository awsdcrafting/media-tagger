from dataclasses import dataclass, field
from typing import List, Set

from dataclasses_json import dataclass_json

from tag import Tag


@dataclass_json
@dataclass
class Media:
    name: str
    media_type: str
    file_hash: str
    file_path: str
    tag_categories: Set[str] = field(default_factory=set)
    tags: List[Tag] = field(default_factory=list)
    media_id: int = -1
