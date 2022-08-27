from dataclasses import dataclass
from typing import Callable, List

from dataclasses_json import dataclass_json

from data.media import Media
from data.naming_target import NamingTarget, NamingTargetType


@dataclass_json
@dataclass
class NamingInfo:
    targets: List[NamingTarget]
    deliminator: str
    condition: Callable[[Media], bool]

    def generate_name(self, media: Media, file_name, folder_count, global_count):
        if self.condition:
            if not self.condition(media):
                return False, file_name
        name_parts = []
        for target in self.targets:
            if target.target_type == NamingTargetType.TAG_CATEGORY:
                if target.target_names not in media.tag_categories:
                    continue
                res = target.deliminator.join([tag.name for tag in media.tags if tag.category == target.target_names])
                if res:
                    name_parts += [res]
            elif target.target_type == NamingTargetType.TAG:
                res = target.deliminator.join([tag.name for tag in media.tags if tag.name in target.target_names])
                if res:
                    name_parts += [res]
            elif target.target_type == NamingTargetType.FILE_NAME:
                name_parts += [file_name]
            elif target.target_type == NamingTargetType.FOLDER_COUNT:
                name_parts += [folder_count]
            elif target.target_type == NamingTargetType.GLOBAL_COUNT:
                name_parts += [global_count]
            pass
        return True, self.deliminator.join(name_parts)
