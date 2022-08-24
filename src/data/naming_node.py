from dataclasses import dataclass

from dataclasses_json import dataclass_json

from src.data.naming_info import NamingInfo


@dataclass_json
@dataclass
class NamingNode:
    info: NamingInfo
    next_node: 'NamingNode'
    alternative: 'NamingNode'
